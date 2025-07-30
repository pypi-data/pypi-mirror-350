from fastapi import Request
from loguru import logger
import traceback
from typing import List, Any

from fastpluggy.core.database import get_db


class ViewBuilder:
    def __init__(self):
        self.templates = None

    def generate(self, request: Request, items: List[Any], **kwargs) -> Any:
        """
        Generate the response for the given request and items.

        Args:
            request (Request): The current HTTP request.
            items (List[Any]): A list of view components to include in the response.

        Returns:
            Any: The rendered template response.
        """
        context = {
            "request": request,
            "title": kwargs.get("title", None),
        }

        rendered_items = []
        for item in items:
            try:
                # Inject request and db if available
                if hasattr(item, "request"):
                    item.request = request
                if hasattr(item, "db"):
                    item.db = next(get_db())
                if hasattr(item, "process"):
                    item.process(request=request, **kwargs)

                # If item provides a render method, call it
                if hasattr(item, "render") and callable(item.render):
                    rendered = item.render(request)

                    # If it returns a (template_name, context) tuple, wrap as custom_template
                    rendered_items.append({
                        "type": "custom_template",
                        "template_name": rendered['template_name'],
                        "context": rendered['context'],
                    })
                    continue  # Skip the rest of the classic processing

                # If classic context injection is present
                if hasattr(item, "context"):
                    context.update(item.context)

                rendered_items.append(item)

            except Exception as e:
                logger.exception(f"Failed to process component {item}: {e}", exc_info=True)
                rendered_items.append(self._generate_error_component(item, e))

        context["item_views"] = rendered_items

        return self.templates.TemplateResponse(
            "components/generic_page.html.j2", context
        )

    @staticmethod
    def _generate_error_component(item, error):
        """
        Generate a placeholder component for failed items.

        Args:
            item: The original item that failed.
            error: The error message to display.

        Returns:
            dict: A placeholder component with the error message.
        """
        error_message = str(error)
        return {
            "type": "error",
            "title": f"Error in {type(item).__name__}",
            "error_message": error_message,
            "traceback": traceback.format_exception(error).__str__(),
            "traceback_str": ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        }
