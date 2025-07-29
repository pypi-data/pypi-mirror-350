from mantarix.core.elevated_button import ElevatedButton


class FilledTonalButton(ElevatedButton):
    """
    A filled tonal button is an alternative middle ground between FilledButton and OutlinedButton buttons. They’re useful in contexts where a lower-priority button requires slightly more emphasis than an outline would give, such as "Next" in an onboarding flow. Tonal buttons use the secondary color mapping.

    Example:
    ```
    import mantarix as mx


    def main(page: mx.Page):
        page.title = "Basic filled tonal buttons"
        page.add(
            mx.FilledTonalButton(text="Filled tonal button"),
            mx.FilledTonalButton("Disabled button", disabled=True),
            mx.FilledTonalButton("Button with icon", icon="add"),
        )

    mx.app(target=main)
    ```

    -----

    Online docs: https://mantarix.dev/docs/controls/filledtonalbutton
    """

    def _get_control_name(self):
        return "filledtonalbutton"
