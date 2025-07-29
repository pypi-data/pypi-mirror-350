from typing import Optional, Any

from fastpluggy.core.view_builer.components import AbstractComponentView


class RawView(AbstractComponentView):
    """
    A custom view that imports a template and dynamically sets data in its context.
    """
    type = "raw"

    def __init__(
            self,
            source: str,
    ):

        self.source = source

    def process(self, item: Optional[Any] = None, **kwargs) -> dict:
        return {
            "type": self.type,
            "source": self.source,
        }