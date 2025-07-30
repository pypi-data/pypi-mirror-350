import json
from typing import Any, Optional

from fastpluggy.core.tools.serialize_tools import serialize_value
from fastpluggy.core.view_builer.components import AbstractComponentView


class DebugView(AbstractComponentView):
    """
    A component to render JSON data for debugging purposes.
    """
    type = "debug"
    template_name = "components/debug/json.html.j2"

    def __init__(self, data: Any, title: Optional[str] = None,  **kwargs):
        """
        Initialize the DebugView component.

        Args:
            data (Any): The data to render as JSON.
            title (Optional[str]): An optional title for the debug view.
            collapsed (bool): Whether the debug view should be collapsed by default.
        """
        self.data = data
        self.title = title or "Debug Information"
        super().__init__(**kwargs)

    def process(self, **kwargs) -> None:
        """
        Process the data and prepare it for rendering.
        """
        self.json_data = json.dumps(serialize_value(self.data), indent=4)