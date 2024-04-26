"""The home page of the app."""
from html import escape
from elasticsearch import Elasticsearch
from dd2477_group_project import styles
from dd2477_group_project.templates import template
from dd2477_group_project.components import podcast
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
#from elastic import search

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

list_of_podcasts = [
    {
        "heading": "Podcast 1",
        "transcript": "This is the transcript for podcast 1",
        "startTime": "3",
        "endTime": "93"
    },
    {
        "heading": "Podcast 2",
        "transcript": "This is the transcript for podcast 2",
        "startTime": "20",
        "endTime": "110"
    },
    {
        "heading": "Podcast 3",
        "transcript": "This is the transcript for podcast 3",
        "startTime": "39",
        "endTime": "129"
    },
    {
        "heading": "Podcast 4",
        "transcript": "This is the transcript for podcast 4",
        "startTime": "160",
        "endTime": "250"
    },
    {
        "heading": "Podcast 5",
        "transcript": "This is the transcript for podcast 5",
        "startTime": "124",
        "endTime": "114"
    },
    {
        "heading": "Podcast 6",
        "transcript": "This is the transcript for podcast 6",
        "startTime": "1403",
        "endTime": "1493"
    },
    {
        "heading": "Podcast 7",
        "transcript": "This is the transcript for podcast 7",
        "startTime": "39",
        "endTime": "39"
    },
    {
        "heading": "Podcast 8",
        "transcript": "This is the transcript for podcast 8",
        "startTime": "39",
        "endTime": "39"
    },
    {
        "heading": "Podcast 9",
        "transcript": "This is the transcript for podcast 9",
        "startTime": "39",
        "endTime": "39"
    },
    {
        "heading": "Podcast 10",
        "transcript": "This is the transcript for podcast 10",
        "startTime": "39",
        "endTime": "39"
    }
]

list_of_podcasts_cars = [
    {
        "heading": "Car Talk Show",
        "transcript": "Rev up your engines and get ready for a wild ride with the Car Talk Show! We'll discuss everything from classic cars to the latest models, and share tips on how to keep your vehicle running smoothly.",
        "startTime": "34",
        "endTime": "0"
    },
    {
        "heading": "Speed Demon Podcast",
        "transcript": "Buckle up and hold on tight! The Speed Demon Podcast is here to satisfy your need for speed. Join us as we explore the world of high-performance cars and share thrilling stories from the racetrack.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Road Trip Chronicles",
        "transcript": "Hit the road with the Road Trip Chronicles podcast! We'll take you on a virtual journey through scenic routes, hidden gems, and unforgettable adventures. Get ready to discover the joy of exploring the world on four wheels.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Off-Road Adventures",
        "transcript": "Leave the pavement behind and venture into the wild with the Off-Road Adventures podcast. Join us as we explore rugged terrains, conquer challenging trails, and share tips on how to navigate the great outdoors.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Vintage Car Tales",
        "transcript": "Step back in time with the Vintage Car Tales podcast. We'll dive into the fascinating history of classic cars, share stories of iconic models, and celebrate the timeless beauty of vintage automobiles.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Supercar Showdown",
        "transcript": "Get ready for an adrenaline-fueled showdown in the world of supercars! The Supercar Showdown podcast brings you the latest news, reviews, and jaw-dropping performances from the most powerful and luxurious vehicles on the planet.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Car Maintenance 101",
        "transcript": "Learn the ins and outs of car maintenance with the Car Maintenance 101 podcast. From changing oil to replacing brake pads, we'll provide step-by-step guides and expert tips to help you keep your car in top shape.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Electric Revolution",
        "transcript": "Join the Electric Revolution and discover the future of transportation. The Electric Revolution podcast explores the world of electric vehicles, renewable energy, and sustainable mobility solutions.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Dream Car Chronicles",
        "transcript": "Embark on a journey through the world of dream cars with the Dream Car Chronicles podcast. We'll showcase the most luxurious, exotic, and awe-inspiring vehicles ever created, and explore the stories behind them.",
        "startTime": "0",
        "endTime": "0"
    },
    {
        "heading": "Cars go Wromm Wromm",
        "transcript": "Also his Cars full of donuts. Oh, that's a good point. That's a good point actually.",
        "startTime": "0",
        "endTime": "0"
    },
]


PodcastItemType = Dict[str, Union[str, int]]

class FormState(rx.State):
    form_data: dict = {}
    result: list[PodcastItemType] = list_of_podcasts_noResult

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data.get('phrase')
        
        
        if self.form_data == "car" or self.form_data == "cars":
            result = list_of_podcasts_cars
        else:
            result = list_of_podcasts

        self.handle_result(result)
        #result = search(self.form_data)
        
    def handle_result(self, result):
        self.result = result



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
                size="8",
                style={"padding-top": 30, "padding-bottom": 20},
            ),
            rx.text("Top 10 Results", class_name="text-start w-[80vw] lg:w-[60vw] font-bold pl-5 pb-3"),
        rx.flex(
            rx.stack(
                rx.accordion.root(
                    rx.accordion.item(
                        header=(rx.text(f"1: {(FormState.result[0]['heading'])} ", class_name="text-xl font-bold")),
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
                        header=(rx.text(f"2: {(FormState.result[1]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[1]['startTime'])} "),
                                rx.text((FormState.result[1]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"3: {(FormState.result[2]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[2]['startTime'])} "),
                                rx.text((FormState.result[2]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"4: {(FormState.result[3]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[3]['startTime'])} "),
                                rx.text((FormState.result[3]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"5: {(FormState.result[4]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[4]['startTime'])} "),
                                rx.text((FormState.result[4]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"6: {(FormState.result[5]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[5]['startTime'])} "),
                                rx.text((FormState.result[5]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"7: {(FormState.result[6]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[6]['startTime'])} "),
                                rx.text((FormState.result[6]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"8: {(FormState.result[7]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[7]['startTime'])} "),
                                rx.text((FormState.result[7]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"9: {(FormState.result[8]['heading'])}", class_name="text-xl font-bold")),
                        content=(
                            rx.stack(
                                rx.text(f"Meantioned at: {(FormState.result[8]['startTime'])} "),
                                rx.text((FormState.result[8]['transcript']), class_name="text-sm"),
                                flex_direction="column",
                            )
                        ),
                    ),
                    rx.accordion.item(
                        header=(rx.text(f"10: {(FormState.result[9]['heading'])}", class_name="text-xl font-bold")),
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


