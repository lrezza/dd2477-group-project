from elasticsearch import Elasticsearch, helpers
import os
import json
from tqdm import tqdm
import csv

podcast_data_dir = "../podcasts-no-audio-13GB/spotify-podcasts-2020"

def main():
    while(True):
        print("What do you want to do?")
        print("1. Re-index windows")
        print("2. Re-index episodes")
        print("3. Exit")
        answer = input("Choose option 1/2/3: ")

        if answer == "1":
            while(True):
                answer = input("Are you sure? This process deletes the current windows index immediately and re-indexing might take a long time (y/n): ")
                if answer == "y":
                    index_windows()
                    return
                elif answer == "n":
                    break
        elif answer == "2":
            while(True):
                answer = input("Are you sure? This process deletes the current episodes index immediately and re-indexing might take a long time (y/n): ")
                if answer == "y":
                    index_episodes()
                    return
                elif answer == "n":
                    break
        elif answer == "3":
            break
        else:
            print("Type either 1, 2 or 3")

def index_windows():
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

    print("Starting window indexing...")
    process_podcast_files(es)

def index_episodes():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    #clear previous indices if exists
    if es.indices.exists(index="episodes"):
        es.indices.delete(index="episodes")

    #setup mappings and settings
    episodes_config = {
        "mappings": {
            "properties": {
                "show_uri": {  
                    "type": "keyword"
                },
                "show_name": {
                    "type": "text"
                },
                "show_description": {
                    "type": "text"
                },
                "publisher": {
                    "type": "text"
                },
                "language": {
                    "type": "keyword"
                },
                "rss_link": {
                    "type": "keyword"
                },
                "episode_uri": {
                    "type": "keyword"
                },
                "episode_name": {
                    "type": "text"
                },
                "episode_description": {
                    "type": "text"
                },
                "duration": {
                    "type": "text"
                }
            }
        }
    }    

    #create new indices
    es.indices.create(index="episodes", body=episodes_config)

    print("Starting episode indexing...")
    process_metadata(es)

def process_podcast_files(es):
    directory = podcast_data_dir + "/podcasts-transcripts"
    filepaths = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
    docs = []
    for filepath in tqdm(filepaths, desc="Indexing", unit="episode"):
        docs += process_windows(filepath, es)
    
        if len(docs) >= 5000:
            helpers.bulk(es, docs)
            docs = []
        
def process_windows(filepath, es):
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
    
def process_metadata(es):
    # Replace 'your_file.tsv' with the path to your TSV file
    file_path = podcast_data_dir + "/metadata.tsv"

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        
        first_row = True
        rows = []
        for row in tsv_reader:
            if first_row:
                first_row = False
            else:
                rows.append(row)

        for row in tqdm(rows, desc="Indexing", unit="episode"):
            episode_doc = {
                "show_uri": row[10],
                "show_name": row[1],
                "show_description": row[2],
                "publisher": row[3],
                "language": row[4],
                "rss_link": row[5],
                "episode_uri": row[11],
                "episode_name": row[7],
                "episode_description": row[8],
                "duration": row[9]
            }

            es.index(index="episodes", document=episode_doc)

if __name__=='__main__':
    main()