"""The home page of the app."""
from elasticsearch import Elasticsearch
from dd2477_group_project import styles
from dd2477_group_project.templates import template
from dd2477_group_project.components import podcast

import reflex as rx

import sys
import os
sys.path.append(os.path.abspath("../../"))
from elastic import search

search.test()

def connect_to_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    if not es.indices.exists(index="windows"):
        raise ValueError("Episode index does not exist, run indexer.py")
    
    return es

def search(words):
    es = connect_to_elastic()
    response = query_episodes(words, es)
    #print(response) # Prints out the full response
    responsetest = response['hits']['hits']
    first_hit = response['hits']['hits'][0]
    only_text = first_hit.get('fields', {}).get('transcript')
    return only_text

class FormState(rx.State):
    form_data: dict = {}
    result: dict = {}

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data.get('phrase')
        #print(self.form_data)
        result = search(self.form_data)
        self.handle_result(result)
        #response = query_episodes(self.form_data, self.es)  # Fix: Pass self.es as an argument
        
    def handle_result(self, result):
        self.result = result
        render_podcasts(result)

"""
def create_podcastlist(result):
    print(len(result))
    podcast_list = [
        {"heading": heading_list,
        "transcript": transcript_list}
    ]
    for i in range(len(result)):
        print(result[i].get('fields', {}).get('transcript'))
    return
"""
    
def render_podcasts(result):
    #print(result)
    print(result)
    return 
    #podcast("TestHeader", result[0].get('fields', {}).get('transcript'))
    """
    return rx.foreach(
        rx.podcast(item.get('fields', {}).get('transcript')),
        for item in result
    )
    """

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
                rx.heading("Search Results", size="7",
                           style={"padding-top": 30, "padding-bottom": 20},
                ),
            #rx.text()
            rx.text(FormState.result[0].to_string(), class_name="w-[80vw] lg:w-[50vw]"),
            #rx.fragment(*render_podcasts(FormState.result)),
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


def query_episodes(word, es):
    # Define the nested query
    max_response_size = 10

    query = {
        "query": {
            "nested": {
                "path": "words",
                "query": {
                    "match": {
                        "words.word": word
                    }
                }
            }
        },

        "fields": ['episode_uri', 'window_index', 'transcript'],
        "_source":False,
        "size": max_response_size,
    }

    response = es.search(index="windows", body=query)
    return response

