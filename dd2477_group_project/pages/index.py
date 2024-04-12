"""The home page of the app."""

from dd2477_group_project import styles
from dd2477_group_project.templates import template

import reflex as rx

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

@template(route="/", title="Podcast Search")
def index() -> rx.Component:
    """The home page.
    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Podcast Search", 
                   class_name="text-green-700 text-center w-full",
                   size="9"
                   ),
        rx.text("Wouldn’t it be great to find podcasts that discuss exactly what you are interested in at the moment? Or even better, to find the exact part of the podcast that discusses your topic of interest?",
                class_name="pt-6 pb-16 text-xl text-center w-[400px] md:w-[700px] xl:w-[900px]",
                ),
        rx.form(
            rx.hstack(
                rx.vstack(
                    rx.input(
                        placeholder="Search Topic",
                        name="phrase",
                        size="3",
                        style={"minWidth": 400},
                        #min_length="1"
                    ),
                    
                    #rx.hstack(
                    #    rx.text("Some specific toggle:"),
                    #    rx.hstack(
                    #        rx.switch("Switched", name="switch"),
                    #    ),
                    #),
                    
                ),
                rx.button("Search", type="submit", color_scheme="grass", size="3"),
                spacing="7",
                style={"margin-bottom": 50}
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
            
        ),
            rx.divider(),
                rx.heading("Search Results",
                           style={"padding-top": 30},
                ),
            rx.text(FormState.form_data.to_string()
        ),
        rx.box(
            rx.link(
                rx.text("Docs"),
                href="https://github.com/lrezza/dd2477-group-project",
                style=styles.link_style,
                class_name="",
                size="4",
            ),
            class_name="w-[94vw] border-solid border-t-2 fixed bottom-0 py-2",
        ),
        class_name="",
        justify="center",
        align="center",
        spacing="2"
    )

