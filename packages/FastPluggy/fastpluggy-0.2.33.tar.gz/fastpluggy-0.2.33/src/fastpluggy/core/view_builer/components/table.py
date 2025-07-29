import traceback
from typing import Any, Callable, Dict, List, Optional, Union
from urllib.parse import urlencode

from fastapi import Request
from loguru import logger

from fastpluggy.core.models_tools.pydantic import ModelToolsPydantic
from fastpluggy.core.models_tools.shared import ModelToolsShared
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from fastpluggy.core.view_builer.components import AbstractComponentView, FieldHandlingView
from fastpluggy.core.view_builer.components.custom import CustomTemplateView
from fastpluggy.core.view_builer.form_builder import FORM_FIELD_MAPPING
from fastpluggy.core.view_builer.components.button import AbstractButtonView, ButtonView

FILTER_WIDGET_MAPPING = FORM_FIELD_MAPPING
FILTER_WIDGET_MAPPING.update(
    {
        # "string": "string",
        # "int": "number",
        # "float": "number",
        # "bool": "select",
        # "date": "date",
        # "enum": "select",
    }
)


class TableView(AbstractComponentView, FieldHandlingView):
    """
    A class representing a table view component.
    """
    type = 'table'

    request: Request

    def __init__(
            self,
            data: List[Dict[str, Any]],
            title: Optional[str] = None,
            fields: Optional[List[str]] = None,
            headers: Optional[Dict[str, str]] = None,
            exclude_fields: Optional[List[Union[str, Any]]] = None,
            links: Optional[List[Union[AbstractButtonView, Dict[str, Any]]]] = None,
            field_callbacks: Optional[Dict[Union[str, Any], Callable[[Any], Any]]] = None,
            request: Request = None,
            **kwargs
    ):
        self.fields = self.process_fields_names(fields or [])  # Define which fields to display
        self.headers = headers or {}  # Custom headers for selected fields
        self.exclude_fields = self.process_fields_names(exclude_fields or [])
        self.field_callbacks = self.process_field_callbacks(field_callbacks or {})
        self.links = links or []
        self.data = data  # Data should already be a list of dictionaries
        self.request = request
        self.params = kwargs
        self.title = title

        super().__init__(**kwargs)


    def _auto_detect_fields_and_headers(self, model):
        """
        Auto-detect fields and generate headers dynamically for the table.
        """
        if model:

            fields_metadata = ModelToolsShared.get_model_metadata(model, self.exclude_fields)

            # Get field names and generate headers
            detected_fields = list(fields_metadata.keys())

            headers = {
                field: self.headers.get(field, field.replace("_", " ").title())
                for field in detected_fields
            }

            return detected_fields, headers
        else:
            return [], {}

    def _build_sortable_headers(self) -> List[Dict[str, Any]]:
        """
        Builds sortable headers for the table.
        If fields are None, headers are created using auto-detected values.
        """
        sortable_headers = []

        # Extract sorting parameters from query
        sort_by = self.get_query_param("sort_by", None, str)
        sort_order = self.get_query_param("sort_order", "asc", str)

        existing_params = dict(self.request.query_params) if self.request and self.request.query_params else {}

        for field in self.fields:
            header_label = self.headers.get(field, field.replace("_", " ").title())
            is_sorted = field == sort_by
            new_order = "desc" if is_sorted and sort_order == "asc" else "asc"

            # Build query parameters for sorting
            updated_params = existing_params.copy()
            updated_params["sort_by"] = field
            updated_params["sort_order"] = new_order

            # Generate sorting URL
            url = None
            if self.request:
                base_url = self.request.url.path
                url = f"{base_url}?{urlencode(updated_params)}"

            sortable_headers.append({
                "label": header_label,
                "url": url,
                "sorted": is_sorted,
                "order": sort_order if is_sorted else None
            })

        return sortable_headers

    def _preprocess_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process data to exclude specified fields.
        """
        processed_data = []
        if data:
            for item in data:
                if ModelToolsPydantic.is_model_instance(item):
                    processed_item = {
                        key: value for key, value in item.model_dump().items() if key not in self.exclude_fields
                    }
                elif ModelToolsSQLAlchemy.is_sqlalchemy_model_instance(item):
                    processed_item = ModelToolsSQLAlchemy.model_to_dict(item, exclude_fields=self.exclude_fields)
                elif hasattr(item, '__dict__'):
                    processed_item = {
                        key: value for key, value in item.__dict__.items() if key not in self.exclude_fields
                    }
                else:
                    processed_item = {
                        key: value for key, value in item.items() if key not in self.exclude_fields
                    }
                processed_data.append(processed_item)
        return processed_data

    def process_fields_and_headers(self, data_or_model: Any):

        if not self.fields:
            self.fields, self.headers = self._auto_detect_fields_and_headers(data_or_model)
        elif self.fields and not self.headers:
            self.fields = self.process_fields_names(self.fields or [])
            self.headers = {
                field: self.headers.get(field, field.replace("_", " ").title())
                for field in self.fields
            }

    def process(self, **kwargs) -> None:
        """
        Process the table view by preparing fields, headers, and data.
        """
        self.data = self._preprocess_data(self.data)  # Data should already be a list of dictionaries

        # Detect fields and headers dynamically if not provided
        self.process_fields_and_headers(self.data)

        # Build sortable headers
        self.headers = self._build_sortable_headers()

        # Apply field-specific callbacks to format field values
        self._apply_field_callbacks()

        # Additional parameters
        self.params = kwargs

    def _apply_field_callbacks(self):
        """
        Apply field-specific callback functions to format field values.
        """
        for item in self.data:
            for field, callback in self.field_callbacks.items():
                if field in item:
                    item[field] = callback(item[field])

    def get_buttons_for_item(self, item: Dict[str, Any]) -> list[dict]:
        """
        Get the list of links/buttons for a specific item.
        """
        buttons = []

        for link in self.links:
            try:
                if isinstance(link, AbstractButtonView) or isinstance(link, CustomTemplateView):
                    if hasattr(link, "request"):
                        link.request = self.request
                    buttons.append(link.process(item))
                elif isinstance(link, dict):
                    # Process using ButtonView
                    button_view = ButtonView(**link)
                    buttons.append(button_view.process(item))
                else:
                    raise ValueError("Unsupported link type in links.")
            except Exception as e:
                logger.exception(traceback.format_exc())
                # Catch and log button processing errors
                logger.error(f"Error processing button for item {item}: {e}")
                buttons.append({
                    "type": "error",
                    "message": f"Error processing button: {e}",
                    "item_id": item.get("id", "Unknown"),
                })
        return buttons
