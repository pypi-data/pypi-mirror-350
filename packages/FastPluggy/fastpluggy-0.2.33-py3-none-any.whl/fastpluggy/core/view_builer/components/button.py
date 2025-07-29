import inspect
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional

from fastpluggy.core.tools import convert_param_type
from fastpluggy.core.tools.fastapi import inspect_fastapi_route
from fastpluggy.core.tools.inspect_tools import is_internal_dependency
from fastpluggy.core.view_builer.components import AbstractComponentView


class ButtonViewMixin:
    """
    A mixin providing common button utilities like condition evaluation, placeholder replacement,
    and parameter processing.
    """

    @staticmethod
    def replace_placeholders(template: str, item: Optional[Dict[str, Any]] = None) -> str:
        if item and "<" in template and ">" in template:
            for key, value in item.items():
                placeholder = f"<{key}>"
                template = template.replace(placeholder, str(value))
        return template

    @staticmethod
    def evaluate_condition(condition: bool | Callable, item: Optional[Dict[str, Any]]) -> bool:
        return condition(item) if callable(condition) else condition

    @staticmethod
    def evaluate_label(label: str | Callable, item: Optional[Dict[str, Any]]) -> str:
        return label(item) if callable(label) else label

    @staticmethod
    def process_params(params: Dict[str, Any], item: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process parameters, replacing placeholders with actual values.
        """
        if params is None:
            return {}

        return {
            key: ButtonViewMixin.replace_placeholders(value, item) if isinstance(value, str) else value
            for key, value in params.items()
        }


class AbstractButtonView(AbstractComponentView, ButtonViewMixin):
    """
    Abstract base class for button views.
    """
    type = "button"

    def __init__(
            self,
            label: Optional[str | Callable] = None,
            css_class: Optional[str | Callable] = None,
            condition: bool | Callable[[Optional[Dict[str, Any]]], bool] = True,
            onclick: Optional[str] = None,
            method: Optional[str] = None,
            params: Optional[Dict[str, Any]] = None,
            # todo: add icon
            **kwargs
    ):
        """
                :param label: Label for the button.
                :param css_class: CSS class for the button.
        """
        self.label = label
        self.params = kwargs
        self.css_class = css_class or 'btn btn-primary'
        self.condition = condition
        self.onclick = onclick
        self.method = method
        self.method = method or "get"
        self.params = params or {}

    def common_process(self, item: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Standardized process method to be shared across all button views.
        """
        return {
            "label": self.evaluate_label(self.label, item),
            "css_class": self.evaluate_label(self.css_class, item),
            "condition": self.evaluate_condition(self.condition, item),
            "onclick": self.onclick,
            "method": self.method,
            "params": self.process_params(self.params, item),
        }

    @abstractmethod
    def process(self, item: Optional[Dict[str, Any]] = None, **kwargs, ) -> Dict[str, Any]:
        """
        Abstract method to process buttons, should be implemented by subclasses.
        """
        raise NotImplementedError

    def _resolve_param_value(self, name: str, item: Optional[dict[str, Any]], default: Any) -> Any:
        source = self.param_inputs.get(name, None)
        run_as_task = getattr(self, "run_as_task", False)

        # If the input is a placeholder like "<id>", resolve it from the item
        if isinstance(source, str) and source.startswith("<") and source.endswith(">"):
            key = source[1:-1]
            if item and key in item:
                return item[key]
            else:
                return default if run_as_task else self._raise_missing(name, key, item)

        # If the input is a static value, return it
        if source is not None:
            return source

        # Fallback to item direct lookup if no placeholder is used
        # If you don’t explicitly define a mapping using <...> syntax,
        # but the parameter name matches a key in the item directly.
        if item and name in item:
            return item[name]

        # Use default if defined
        if default != inspect.Parameter.empty:
            return default

        if not run_as_task:
            self._raise_missing(name, name, item)

    def _raise_missing(self, param_name: str, lookup_key: str, item: Optional[dict[str, Any]]):
        raise ValueError(
            f"Missing required parameter '{param_name}'. Tried looking for '{lookup_key}' in item, "
            f"got: {list(item.keys()) if item else 'None'}"
        )


class ButtonView(AbstractButtonView):
    """
    A class representing a set of action buttons.
    """
    type = "buttons"

    def __init__(
            self,
            url: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.url = url

    def process(self, item: Optional[Dict[str, Any]] = None, **kwargs, ) -> dict[str, Any]:
        """
        Process buttons by replacing placeholders and evaluating conditions.
        """
        data = super().common_process(item, **kwargs)
        data.update({
            "url": self.replace_placeholders(self.url, item),
        })
        return data


class FunctionButtonView(AbstractButtonView):
    """
    A class representing a button defined by a function to be executed via an executor endpoint.
    """
    type = "function_button"

    def __init__(
            self,
            call: Callable,
            param_inputs: Optional[Dict[str, Any]] = None,
            run_as_task: bool = False,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.call = call
        self.label = self.label or call.__name__.replace('_', ' ').capitalize()
        self.method = 'post'
        self.param_inputs = param_inputs or {}
        self.run_as_task = run_as_task

    def process(self, item: Optional[Dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        data = super().common_process(item, **kwargs)

        url = f"/execute/{self.call.__qualname__}"
        # Generate the params
        params = self._generate_params(item)
        params['_module'] = self.call.__module__
        params['_function'] = self.call.__name__

        data.update({
            "url": url,
            "params": params,
        })
        return data

    def _generate_params(self, item: Optional[dict[str, Any]]) -> dict[str, Any]:
        sig = inspect.signature(self.call)
        params_dict = {}

        for name, param in sig.parameters.items():
            if is_internal_dependency(param.annotation):
                continue

            value = self._resolve_param_value(name, item, param.default)
            if value is not None:
                params_dict[name] = convert_param_type(param.annotation, value)

        if self.run_as_task:
            params_dict['_run_as_task'] = 'true'

        return params_dict


class AutoLinkView(AbstractButtonView):
    """
    A class that generates links dynamically by mapping table columns to FastAPI endpoint parameters.

    This class uses the `inspect_fastapi_route` utility to detect the HTTP method,
    path parameters, and query parameters of a given FastAPI route. It then dynamically
    generates URLs based on the provided `item` data.
    """

    type = "auto_link"
    request = None

    def __init__(
            self,
            route_name: str,
            param_inputs: Optional[Dict[str, Any]] = None,
            **kwargs
    ):
        """
        Initialize the AutoLinkView.
        :param route_name: The FastAPI endpoint route (function name).
        :param label: Label for the button.
        :param method: HTTP method for the link; auto-detected if not provided.
        :param condition: Optional condition to display the button.
        :param kwargs: Additional parameters.
        """
        super().__init__(**kwargs)
        self.route_name = route_name
        self.param_inputs = param_inputs or {}
        self.label = self.label or route_name.replace('_', ' ').capitalize()

    def process(self, item: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate the link dynamically.
        :param item: The data item being processed.
        :return: List of processed links.
        """
        # Inject request if available
        if 'request' in kwargs:
            self.request = kwargs['request']

        # Detect the route method and parameters using the updated inspect_fastapi_route
        route_metadata = inspect_fastapi_route(
            app=self.request.app,
            route_name=self.route_name
        )

        # Extract relevant data from the route metadata
        method = route_metadata["methods"][0] if route_metadata["methods"] else None
        path_param_names = route_metadata["path_params"]
        query_param_names = route_metadata["query_params"]
        body_param_names = route_metadata["body_params"]

        matched_params = self._match_params(
            param_names=path_param_names + query_param_names + body_param_names,
            item=item
        )

        # Separate path and query parameters
        path_params = {param['name']: matched_params[param['name']] for param in route_metadata["path_params"] if
                       param['name'] in matched_params}
        query_params = {param['name']: matched_params[param['name']] for param in route_metadata["query_params"] if
                        param['name'] in matched_params}

        # Construct the URL dynamically using url_for
        url = self._generate_url(path_params, query_params)

        # Process the item and add the generated link metadata
        data = super().common_process(item, **kwargs)
        data.update({
            "url": url,
            "params": matched_params,
            "method": method,
        })
        return data

    def _match_params(self, param_names: List[Dict[str, Any]], item: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Match route parameters to item columns.

        Args:
            param_names (List[Dict[str, Any]]): Parameter descriptors from inspect_fastapi_route
            item (Optional[Dict[str, Any]]): Data item from the table.

        Returns:
            Dict[str, Any]: Matched parameters.

        Skips:
            - Parameters of type 'file'
            - Parameters with a defined default
        """
        matched_params = {}

        for param in param_names:
            name = param['name']
            param_type = param.get('type')
            default = param.get('default')

            # Skip if it's a file input (UploadFile/File)
            if param_type == 'file':
                continue

            # Try to resolve the value
            value = self._resolve_param_value(name, item, default=default)

            # If value is found or a default was given, use it
            if value is not None:
                matched_params[name] = value
            elif default is None:
                continue  # Skip missing optional param
            else:
                raise ValueError(
                    f"Missing required parameter '{name}' for route '{self.route_name}'. "
                    f"Available keys in item: {list(item.keys()) if item else 'None'}, "
                    f"and param_inputs: {list(self.param_inputs.keys()) if self.param_inputs else 'None'}."
                )

        return matched_params

    def _generate_url(self, path_params: Dict[str, Any], query_params: Dict[str, Any]) -> str:
        """
        Generate the URL with query parameters from matched params.

        Args:
            path_params (Dict[str, Any]): Path parameters for the URL.
            query_params (Dict[str, Any]): Query parameters for the URL.

        Returns:
            str: The generated URL.

        Raises:
            ValueError: If required path parameters are missing.
        """
        try:
            # Use url_for to generate the URL
            url = self.request.url_for(self.route_name, **path_params)
            if query_params:
                from urllib.parse import urlencode
                url = f"{url}?{urlencode(query_params)}"
            return url
        except Exception as e:
            raise ValueError(f"Error generating URL for route '{self.route_name}': {str(e)}")
