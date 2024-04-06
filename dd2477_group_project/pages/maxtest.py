"""The test page."""

from dd2477_group_project.templates import template
from dd2477_group_project import styles

import reflex as rx


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
