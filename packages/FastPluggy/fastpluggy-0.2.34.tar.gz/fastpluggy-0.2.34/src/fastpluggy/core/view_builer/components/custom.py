from typing import Optional, Any

from fastpluggy.core.view_builer.components import AbstractComponentView


class CustomTemplateView(AbstractComponentView):
    """
    A custom view that imports a template and dynamically sets data in its context.
    """
    type = "custom_template"

    def __init__(
            self,
            template_name: str,
            context: dict = None,
            **kwargs,
    ):
        """
        Initialize the CustomTemplateView.

        Args:
            template_name (str): Name of the Jinja2 template to import.
            context (dict, optional): Context data to pass to the template. Defaults to None.
            **kwargs: Additional parameters for customization.
        """
        self.template_name = template_name
        self.context = context or {}
        self.params = kwargs

    def process(self, item: Optional[Any] = None, **kwargs) -> dict:
        """
        Process the view by updating the context dynamically.

        Args:
            :param item:
            **kwargs: Additional context data to inject.
        """
        # Merge the provided context with any additional parameters
        if item:
            self.context.update({"item": item})
        self.context.update(kwargs)

        return {
            "type": self.type,
            "template_name": self.template_name,
            "context": self.context,
        }