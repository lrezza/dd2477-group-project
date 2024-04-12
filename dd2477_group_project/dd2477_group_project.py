"""Welcome to Reflex!."""

from dd2477_group_project import styles

# Import all the pages.
from dd2477_group_project.pages import *

import reflex as rx


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App(style=styles.base_style)
