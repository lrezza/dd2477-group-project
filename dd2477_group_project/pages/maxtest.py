"""The test page."""

from dd2477_group_project.templates import template
from dd2477_group_project import styles

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
        rx.heading("Podcast Search", 
                   class_name="text-green-700 text-center w-full",
                   size="9"
                   ),
        rx.text("Wouldn’t it be great to find podcasts that discuss exactly what you are interested in at the moment? Or even better, to find the exact part of the podcast that discusses your topic of interest?",
                class_name="pt-4 pb-8 text-xl text-center",
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
                rx.button("Submit", type="submit", class_name="bg-green-700"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
            rx.divider(),
            rx.heading("Results"),
            rx.text(FormState.form_data.to_string()
        ),
        rx.box(
            rx.link(
                rx.text("Docs"),
                href="https://github.com/lrezza/dd2477-group-project",
                style=styles.link_style,
                class_name="",
            ),
            class_name="w-[94vw] border-solid border-t-2 fixed bottom-0 py-2",
        )
    )
