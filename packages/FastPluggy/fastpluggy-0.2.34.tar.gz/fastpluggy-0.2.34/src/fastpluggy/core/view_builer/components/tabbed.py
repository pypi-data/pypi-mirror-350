from typing import List

from fastpluggy.core.view_builer.components import AbstractComponentView


class TabbedView(AbstractComponentView):
    """
    A component that renders multiple tabs.
    Each tab can contain:
     - A list of child components (like TableView or FormView) in 'subitems'
     OR
     - A plain HTML string in 'content'
    """

    type = "tabbed_view"

    def __init__(
            self,
            tabs: List,
            collapsed: bool = False,
    ):
        super().__init__(collapsed=collapsed)
        self.tabs = tabs

    def process(self, request=None, **kwargs) -> None:
        """
        Process each subcomponent in each tab, letting them do their usual logic
        before rendering.
        """
        # If a tab has "subitems", we call .process() on each item
        for tab in self.tabs:
            if hasattr(tab, "hide_header"):
                tab.hide_header = True
            if hasattr(tab, "process"):
                tab.process(request=request, **kwargs)
