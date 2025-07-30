import random
from abc import ABC
from abc import abstractmethod
from typing import Any, List, Dict, Callable, Union

from typing import Optional

from pydantic import BaseModel
from inspect import signature, _empty
from typing import Tuple, Type
from pydantic import create_model

def config_model_from_init(
    view_cls: Type,
) -> Type[BaseModel]:
    sig = signature(view_cls)
    fields: Dict[str, Tuple[Any, Any]] = {}

    # skip 'self'
    for name, param in sig.parameters.items():
        ann = param.annotation if param.annotation is not _empty else Any
        default = param.default if param.default is not _empty else ...
        fields[name] = (ann, default)

    model_name = f"{view_cls.__name__}Config"
    return create_model(model_name, **fields)

class AbstractComponentView(ABC):

    def __init__(self, collapsed: bool = False):

        self.id = random.randint(1, 10000)
        self.collapsed = collapsed
        # usefully when component is used into tabbed one
        self.hide_header = False

        # usefully to add create link for ModelView or TableModelView to create object or to add batch action link
        self.header_links = []

    @abstractmethod
    def process(self, **kwargs) -> None:
        """
        Process method to dynamically inject parameters like request, db, etc.
        """
        raise NotImplementedError

    def get_query_param(self, key: str, default: Any, cast_type: type = int) -> Any:
        """
        Retrieves a query parameter from the request and casts it to the specified type.

        :param key: The key of the query parameter.
        :param default: The default value to return if the parameter is not found or cannot be cast.
        :param cast_type: The type to cast the query parameter to (default: int).
        :return: The query parameter value cast to the specified type, or the default value.
        """
        if self.request and self.request.query_params:
            try:
                return cast_type(self.request.query_params.get(key, default))
            except (ValueError, TypeError):
                return default
        return default

    @classmethod
    def get_definition(cls) -> Dict[str, Any]:
        config_model = config_model_from_init(cls)
        return config_model.model_json_schema()

class FieldHandlingView(ABC):
    """
    Abstract base class for components that handle field processing.
    """

    @staticmethod
    def get_field_name(field: Any) -> str:
        """
        Extract the field name from various field representations.

        Args:
            field (Any): The field representation (string, SQLAlchemy field, etc.).

        Returns:
            str: The extracted field name.

        Raises:
            ValueError: If the field type is unsupported.
        """
        if isinstance(field, str):
            return field
        elif hasattr(field, 'key'):
            return field.key  # SQLAlchemy Column object
        elif hasattr(field, 'fget'):
            return field.fget.__name__  # SQLAlchemy hybrid property
        elif hasattr(field, '__name__'):
            return field.__name__  # Regular property or method
        else:
            raise ValueError(f"Unsupported field type: {field}")

    @staticmethod
    def process_field_callbacks(field_callbacks: dict[Any, Callable[[Any], Any]]) -> dict[Any, Callable[[Any], Any]]:
        """
        Process field_callbacks to ensure keys are field names.
        """
        processed_callbacks = {}
        for key, callback in field_callbacks.items():
            field_name = FieldHandlingView.get_field_name(key)
            processed_callbacks[field_name] = callback
        return processed_callbacks

    @staticmethod
    def process_fields_names(list_fields: List[Any]) -> List[str]:
        """
        Process exclude_fields to ensure they are field names.

        Args:
            list_fields (List[Any]): A list of field names or SQLAlchemy field references.

        Returns:
            List[str]: A list of processed field names.
        """
        return [FieldHandlingView.get_field_name(field) for field in list_fields]


