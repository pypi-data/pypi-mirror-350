from mantarix.core.elevated_button import ElevatedButton


class Button(ElevatedButton):
    """
    Elevated buttons or Buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

    Example:
    ```
    import mantarix as mx

    def main(page: mx.Page):
        page.title = "Basic buttons"
        page.add(
            mx.Button(text="Button"),
            mx.Button("Disabled button", disabled=True),
        )

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/elevatedbutton
    """
