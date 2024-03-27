"""The test page."""

from dd2477_group_project.templates import template

import reflex as rx


@template(route="/maxtest", title="Max Sida")
def maxtest() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Test sida", size="8"),
        rx.text("Detta är lite test text."),
        rx.text(
            "Frontenden ändras här:",
            rx.code(".venv/dd2477_group_project/pages/maxtest.py"),
        ),
    )
