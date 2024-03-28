"""The test page."""

from dd2477_group_project.templates import template

import reflex as rx


class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

@template(route="/maxtest", title="Max Sida")
def maxtest() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Test sida", class_name="text-3xl, text-blue-500"),
        rx.text("Detta är lite test text."),
        rx.text(
            "Frontenden för denna sida ändras här:",
            rx.code(".venv/dd2477_group_project/pages/maxtest.py"),
        ),
        rx.form(
            rx.hstack(
                rx.vstack(
                    rx.input(
                        placeholder="Search Topic",
                        name="phrase",
                    ),
                    rx.hstack(
                        rx.text("Some specific toggle:"),
                        rx.hstack(
                            rx.switch("Switched", name="switch"),
                        ),
                    ),
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
            rx.divider(),
            rx.heading("Results"),
            rx.text(FormState.form_data.to_string()
        ),
    )
