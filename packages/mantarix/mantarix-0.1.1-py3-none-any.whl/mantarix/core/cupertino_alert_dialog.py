from typing import Any, List, Optional

from mantarix.core.control import Control
from mantarix.core.ref import Ref
from mantarix.core.types import OptionalControlEventCallable


class CupertinoAlertDialog(Control):
    """
    An iOS-style alert dialog.
    An alert dialog informs the user about situations that require acknowledgement. An alert dialog has an optional title and an optional list of actions. The title is displayed above the content and the actions are displayed below the content.

    Example:
    ```
    import mantarix as mx


    def main(page: mx.Page):
        page.horizontal_alignment = mx.CrossAxisAlignment.CENTER
        page.scroll = True

        def handle_action_click(e):
            page.add(mx.Text(f"Action clicked: {e.control.text}"))
            # e.control is the clicked action button, e.control.parent is the corresponding parent dialog of the button
            page.close(e.control.parent)

        cupertino_actions = [
            mx.CupertinoDialogAction(
                "Yes",
                is_destructive_action=True,
                on_click=handle_action_click,
            ),
            mx.CupertinoDialogAction(
                text="No",
                is_default_action=False,
                on_click=handle_action_click,
            ),
        ]

        material_actions = [
            mx.TextButton(text="Yes", on_click=handle_action_click),
            mx.TextButton(text="No", on_click=handle_action_click),
        ]

        page.add(
            mx.FilledButton(
                text="Open Material Dialog",
                on_click=lambda e: page.open(
                    mx.AlertDialog(
                        title=mx.Text("Material Alert Dialog"),
                        content=mx.Text("Do you want to delete this file?"),
                        actions=material_actions,
                    )
                ),
            ),
            mx.CupertinoFilledButton(
                text="Open Cupertino Dialog",
                on_click=lambda e: page.open(
                    mx.CupertinoAlertDialog(
                        title=mx.Text("Cupertino Alert Dialog"),
                        content=mx.Text("Do you want to delete this file?"),
                        actions=cupertino_actions,
                    )
                ),
            ),
            mx.FilledButton(
                text="Open Adaptive Dialog",
                adaptive=True,
                on_click=lambda e: page.open(
                    mx.AlertDialog(
                        adaptive=True,
                        title=mx.Text("Adaptive Alert Dialog"),
                        content=mx.Text("Do you want to delete this file?"),
                        actions=cupertino_actions if page.platform in [mx.PagePlatform.IOS, mx.PagePlatform.MACOS] else material_actions,
                    )
                ),
            ),
        )


    mx.app(target=main)
    ```
    -----

    Online docs: https://mantarix.dev/docs/controls/cupertinoalertdialog
    """

    def __init__(
        self,
        open: bool = False,
        modal: bool = False,
        title: Optional[Control] = None,
        content: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        on_dismiss: OptionalControlEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        barrier_color: Optional[str] = None
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.modal = modal
        self.title = title
        self.content = content
        self.actions = actions
        self.on_dismiss = on_dismiss
        self.barrier_color = barrier_color

    def _get_control_name(self):
        return "cupertinoalertdialog"

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # open
    @property
    def open(self) -> bool:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self) -> bool:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
    
    #barrier_color
    @property
    def barrier_color(self) -> Optional[str]:
        return self._get_attr("barrierColor")

    @barrier_color.setter
    def barrier_color(self, value: Optional[str]):
        self._set_attr("barrierColor", value)

    # actions
    @property
    def actions(self) -> List[Control]:
        return self.__actions

    @actions.setter
    def actions(self, value: Optional[List[Control]]):
        self.__actions = value if value is not None else []

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalControlEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dismiss", handler)
