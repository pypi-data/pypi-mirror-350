from mantarix.core.elevated_button import ElevatedButton


class FilledButton(ElevatedButton):
    """
    Filled buttons have the most visual impact after the FloatingActionButton (https://mantarix.dev/docs/controls/floatingactionbutton), and should be used for important, final actions that complete a flow, like Save, Join now, or Confirm.

    Example:
    ```
    import mantarix as mx


    def main(page: mx.Page):
        page.title = "Basic filled buttons"
        page.add(
            mx.FilledButton(text="Filled button"),
            mx.FilledButton("Disabled button", disabled=True),
            mx.FilledButton("Button with icon", icon="add"),
        )

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/filledbutton
    """

    def _get_control_name(self):
        return "filledbutton"
