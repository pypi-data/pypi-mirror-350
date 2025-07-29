from typing import Any, Optional

from mantarix.core.control import Control, OptionalNumber
from mantarix.core.ref import Ref
from mantarix.core.types import OptionalControlEventCallable


class RadioGroup(Control):
    """
    Radio buttons let people select a single option from two or more choices.

    Example:
    ```
    import mantarix as mx

    def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = mx.Text()
    b = mx.ElevatedButton(text='Submit', on_click=button_clicked)
    cg = mx.RadioGroup(content=mx.Column([
        mx.Radio(value="red", label="Red"),
        mx.Radio(value="green", label="Green"),
        mx.Radio(value="blue", label="Blue")]))

    page.add(mx.Text("Select your favorite color:"), cg, b, t)

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/radio
    """

    def __init__(
        self,
        content: Control,
        value: Optional[str] = None,
        on_change: OptionalControlEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.value = value
        self.on_change = on_change

    def _get_control_name(self):
        return "radiogroup"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

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
