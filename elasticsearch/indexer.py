from elasticsearch import Elasticsearch, helpers
import pandas as pd
import os
import json
from tqdm import tqdm

podcast_data_dir = "../podcasts-no-audio-13GB/spotify-podcasts-2020"

def main():
    while(True):
        answer = input("Are you sure you want to delete and re-index podcast data? (y/n) ")
        if answer == "y":
            break
        elif answer == "n":
            return
        
    es = setup_elastic()
    index_podcasts(es)

def setup_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    #clear previous indices if exists
    if es.indices.exists(index="windows"):
        es.indices.delete(index="windows")

    #setup mappings and settings
    windows_config = {
        "settings": {
            "index": {"mapping" : {"nested_objects": {"limit": 50000}}},
        },
        "mappings": {
            "properties": {
                "episode_uri": {  
                    "type": "keyword"
                },
                "window_index": {
                    "type": "integer",
                },
                "transcript": {
                    "type": "text"
                },
                "words": {
                    "type": "nested",
                    "properties": {
                        "start_time": {
                            "type": "text"
                        },
                        "end_time": {
                            "type": "text"
                        },
                        "word": {
                            "type": "keyword"
                        }
                    }
                }
            }
        }
    }

    #create new indices
    es.indices.create(index="windows", body=windows_config)

    return es

def index_podcasts(es):
    directory = podcast_data_dir + "/podcasts-transcripts"
    filepaths = []

    print("Starting indexing...")
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
    docs = []
    for filepath in tqdm(filepaths, desc="Indexing", unit="episode"):
        docs += process_episode(filepath, es)
    
        if len(docs) >= 5000:
            helpers.bulk(es, docs)
            docs = []
        
def process_episode(filepath, es):
    with open(filepath, 'r') as file:
        episode_uri = os.path.basename(filepath)[:-5]
        data = json.load(file)

        window_index = 0
        docs = []
        for entry in data["results"]:
            window = entry["alternatives"][0]
            
            if "transcript" in window:
                words = []
                for word_entry in window["words"]:
                    word_doc = {
                        "start_time": word_entry["startTime"],
                        "end_time": word_entry["endTime"],
                        "word": word_entry["word"]
                    }
                    words.append(word_doc)
                window_doc = {
                    "episode_uri": episode_uri,
                    "window_index": window_index,
                    "transcript": window["transcript"],
                    "words": words
                }

                docs.append({"_index": "windows", "_source": window_doc})
                window_index += 1

        return docs

if __name__=='__main__':
    main()