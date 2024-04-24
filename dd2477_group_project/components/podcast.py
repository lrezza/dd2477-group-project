from dd2477_group_project import styles
import reflex as rx

def podcast(heading, transcript) -> rx.Component:

    return rx.box(
        rx.heading(heading, size="4"),
        rx.text(transcript),
    )