from typing import Any, Dict, List, Optional, Union

from fastpluggy.core.view_builer.components import AbstractComponentView
from fastpluggy.core.view_builer.components.button import AbstractButtonView, ButtonView


class ListButtonView(AbstractComponentView):
    type = "button_list"

    def __init__(
            self,
            buttons: List[Union[AbstractButtonView, Dict[str, Any]]],
            title: Optional[str] = None,
            **kwargs
    ):
        self.title = title
        self.params = kwargs
        self.buttons = buttons

        super().__init__(**kwargs)

    def process(self, item=None, **kwargs):
        """
        Dynamically process the buttons with additional parameters.
        """
        list_button = []
        for button in self.buttons:
            if isinstance(button, AbstractButtonView) and hasattr(button, "process"):
                list_button.append(button.process(item=item, **kwargs))
            elif isinstance(button, dict):
                # Process using ButtonView
                button_view = ButtonView(**button)
                processed_buttons = button_view.process(item)
                list_button.append(processed_buttons)
            else:
                raise ValueError("Unsupported link type in links.")

        return list_button
