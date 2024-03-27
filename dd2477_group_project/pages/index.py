"""The home page of the app."""

from dd2477_group_project import styles
from dd2477_group_project.templates import template

import reflex as rx


@template(route="/", title="Podcast Search", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
