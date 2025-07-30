from typing import Optional, Type, Dict, List, Any

from wtforms import Form

from fastpluggy.core.models_tools.shared import ModelToolsShared
from fastpluggy.core.view_builer.components import AbstractComponentView, FieldHandlingView
from fastpluggy.core.view_builer.form_builder import FormBuilder


class FormView(AbstractComponentView, FieldHandlingView):
    """
    A class representing a form view component.
    """
    type = "form"

    form = None

    def __init__(
            self,
            model: Optional[Type[Any]] = None,
            action: str = "",
            method: str = "post",
            fields: Optional[Dict[str, Any]] = None,
            exclude_fields: Optional[List[str]] = None,
            readonly_fields: Optional[List[str]] = None,
            additional_fields: Optional[Dict[str, Any]] = None,
            title: Optional[str] = None,
            submit_label: Optional[str] = "Submit",
            data: Optional = None,  # SQLAlchemy or dict
            **kwargs,
    ):
        """
        Initialize the FormView component.

        Args:
            model (Type[Any], optional): The model to generate the form from.
            action (str): The form submission URL.
            method (str): The form submission method (default: "post").
            exclude_fields (List[str], optional): Fields to exclude from the form.
            readonly_fields (List[str], optional): Fields to make read-only.
            additional_fields (Dict[str, Any], optional): Additional custom fields for the form.
            title (str, optional): The title of the form view.
            submit_label (str): The label for the submit button.
            data (Union[Dict[str, Any], DeclarativeMeta], optional): Data to pre-fill the form fields.
            **kwargs: Additional parameters for the view.
        """
        self.model = model
        self.action = action
        self.method = method
        self.fields = fields or {}
        self.exclude_fields = exclude_fields or []
        self.readonly_fields = readonly_fields or []
        self.additional_fields = additional_fields or {}
        self.title = title
        self.submit_label = submit_label
        self.params = kwargs

        # Convert SQLAlchemy object to a dictionary
        self.data = ModelToolsShared.extract_model_data(data, fields=None, exclude=self.exclude_fields) if data else {}
        self.form = None

    def _generate_form(self) -> Type[Form]:
        """
        Generate a WTForms form class using the FormBuilder.

        Returns:
            Type[Form]: The generated form class.
        """
        if self.fields:
            form_fields = {
                name: field() if callable(field) else field
                for name, field in self.fields.items()
            }
            name = self.model.__name__ if self.model else "Manual"
            return type(f"{name}CustomForm", (Form,), form_fields)

        if not self.model:
            raise ValueError("Model is required to generate a form.")
        return FormBuilder.generate_form(
            model=self.model,
            exclude_fields=self.exclude_fields,
            additional_fields=self.additional_fields,
            readonly_fields=self.readonly_fields,
            # field_widgets: Optional[Dict[str, Any]] = None,
            # field_render_kw: Optional[Dict[str, Dict[str, Any]]] = None,
        )

    def get_form(self, form_data=None) -> Form:
        """
        Get an instance of the WTForms form, optionally populating it with form submission data.

        Args:
            form_data: Form submission data (e.g., `request.form`).

        Returns:
            Form: An instance of the WTForms form.
        """
        self.exclude_fields = self.process_fields_names(self.exclude_fields or [])

        if self.form is None:
            self.form = self._generate_form()(formdata=form_data, data=self.data)
        else:
            self.form.process(formdata=form_data, data=self.data)
        return self.form

    def process(self, form_data=None, **kwargs) -> None:
        """
        Process the view, allowing dynamic parameter injection.

        Args:
            form_data (Dict[str, Any], optional): Data to populate the form with.
            **kwargs: Additional parameters to process.
        """
        self.exclude_fields = self.process_fields_names(self.exclude_fields or [])
        self.get_form(form_data)
