"""The home page of the app."""
from html import escape
from elasticsearch import Elasticsearch
from dd2477_group_project import styles
from dd2477_group_project.templates import template
from typing import List, Dict, Union
import reflex as rx

import sys
import os
import random
import random
import random
import time
import random
sys.path.append(os.path.abspath("../../"))
from elastic import searcher

es = None

list_of_podcasts_noResult = [
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "1:45",
        "endTime": "0"
    },
    {
        "heading": "No result yet",
        "transcript": "No result yet",
        "startTime": "0",
        "endTime": "0"
    }
]



PodcastItemType = Dict[str, Union[str, int]]

class FormState(rx.State):
    form_data: dict = {}
    result: list[PodcastItemType] = list_of_podcasts_noResult

    def handle_submit(self, form_data: dict):
        global es

        """Handle the form submit."""
        self.form_data = form_data.get('phrase')

        query = self.form_data
        result = searcher.get_top_podcast_clips(query, es)
        
        self.handle_result(result)
        #result = search(self.form_data)
        
    def handle_result(self, result):
        self.result = result


@template(route="/", title="Podcast Search")
def index() -> rx.Component:
    global es 
    es = searcher.connect_to_elastic()
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
                size="8",
                style={"padding-top": 30, "padding-bottom": 20},
            ),
            rx.text("Top 10 Results", class_name="text-start w-[80vw] lg:w-[60vw] font-bold pl-5 pb-3"),
        rx.flex(
            rx.stack(
                rx.accordion.root(
                    rx.accordion.item(
                        header=(rx.text(f"1: {(FormState.result[0]['heading'])} ", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[0]['startTime'])} "),
                                rx.text((FormState.result[0]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                        value="item_1",
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"2: {(FormState.result[1]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[1]['startTime'])} "),
                                rx.text((FormState.result[1]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"3: {(FormState.result[2]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[2]['startTime'])} "),
                                rx.text((FormState.result[2]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"4: {(FormState.result[3]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[3]['startTime'])} "),
                                rx.text((FormState.result[3]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"5: {(FormState.result[4]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[4]['startTime'])} "),
                                rx.text((FormState.result[4]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"6: {(FormState.result[5]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[5]['startTime'])} "),
                                rx.text((FormState.result[5]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"7: {(FormState.result[6]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[6]['startTime'])} "),
                                rx.text((FormState.result[6]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"8: {(FormState.result[7]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[7]['startTime'])} "),
                                rx.text((FormState.result[7]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        )
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"9: {(FormState.result[8]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[8]['startTime'])} "),
                                rx.text((FormState.result[8]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"10: {(FormState.result[9]['heading'])}", class_name="text-xl font-bold text-left")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[9]['startTime'])} "),
                                rx.text((FormState.result[9]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    collapsible=True,
                    color_scheme="grass",
                    class_name="w-[80vw] lg:w-[60vw] space-y-2",
                    default_value="item_1",
                    variant="surface",
                    
                ),
                flex_direction="column",
                class_name="w-[80vw] lg:w-[60vw]",
            ),
            class_name="w-[80vw] lg:w-[60vw] z-[0]",
        ),
            
        #rx.text(FormState.result[0].to_string(), class_name="w-[80vw] lg:w-[50vw]"),
        #rx.fragment(*render_podcasts(FormState.result)),
        rx.box(
            rx.link(
                rx.text("Docs"),
                href="https://github.com/lrezza/dd2477-group-project",
                style=styles.link_style,
                class_name="",
                size="4",
            ),
            class_name="w-[94vw] border-solid border-t-2 fixed bottom-0 py-2 bg-white z-[10]",
        ),
        class_name="bg-white",
        justify="center",
        align="center",
        spacing="2",
        style={"background-color": "#ffffff"},
    )


