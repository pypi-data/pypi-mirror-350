from typing import Any, Optional

from mantarix.core.control import Control
from mantarix.core.ref import Ref
from mantarix.core.types import OptionalControlEventCallable


class SelectionArea(Control):
    """
    Mantarix controls are not selectable by default. SelectionArea is used to enable selection for its child control.

    Example:
    ```
    import mantarix as mx

    def main(page: mx.Page):
        page.add(
            mx.SelectionArea(
                content=mx.Column([mx.Text("Selectable text"), mx.Text("Also selectable")])
            )
        )
        page.add(mx.Text("Not selectable"))

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/selectionarea
    """

    def __init__(
        self,
        content: Control,
        on_change: OptionalControlEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.content = content
        self.on_change = on_change

    def _get_control_name(self):
        return "selectionarea"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
