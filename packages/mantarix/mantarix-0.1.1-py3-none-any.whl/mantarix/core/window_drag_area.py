from typing import Any, Optional, Union

from mantarix.core.animation import AnimationValue
from mantarix.core.badge import BadgeValue
from mantarix.core.constrained_control import ConstrainedControl
from mantarix.core.control import Control, OptionalNumber
from mantarix.core.ref import Ref
from mantarix.core.tooltip import TooltipValue
from mantarix.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class WindowDragArea(ConstrainedControl):
    """
    A control for drag to move, maximize and restore application window.

    When you have hidden the title bar with `page.window_title_bar_hidden`, you can add this control to move the window position.

    Example:
    ```
    import mantarix as mx

    def main(page: mx.Page):
        page.window_title_bar_hidden = True
        page.window_title_bar_buttons_hidden = True

        page.add(
            mx.Row(
                [
                    mx.WindowDragArea(mx.Container(mx.Text("Drag this area to move, maximize and restore application window."), bgcolor=mx.colors.AMBER_300, padding=10), expand=True),
                    mx.IconButton(mx.icons.CLOSE, on_click=lambda _: page.window_close())
                ]
            )
        )

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/windowdragarea
    """

    def __init__(
        self,
        content: Control,
        maximizable: Optional[bool] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.maximizable = maximizable

    def _get_control_name(self):
        return "windowDragArea"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # maximizable
    @property
    def maximizable(self) -> bool:
        return self._get_attr("maximizable", data_type="bool", def_value=True)

    @maximizable.setter
    def maximizable(self, value: Optional[bool]):
        self._set_attr("maximizable", value)
