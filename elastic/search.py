from elasticsearch import Elasticsearch
from searcher import *
import math

def get_top_podcast_clips(query, es):
    # Split the input into an array of words
    query_words = query.split()

    # Get top 20 windows based on their transcript scores
    search_result = search_windows_by_transcript(es, query_words)

    # Combine the ranked windows into clips
    clips = create_clips_from_hits(es, search_result['hits']['hits'])

    # Aggregate scores for each clip
    clips_with_scores = [(clip, sum(window['_score'] for window in clip)) for clip in clips]

    # Rank clips based on aggregated scores
    ranked_clips = sorted(clips_with_scores, key=lambda x: x[1], reverse=True)

    # get the top n ranked clips
    n = 10

    podcast_clips = []
    for _rank, (clip, _score) in enumerate(ranked_clips[:n], start=1):
        start_time = clip[0]["_source"]["words"][0]["start_time"]
        end_time = clip[-1]["_source"]["words"][-1]["end_time"]
        transcript = ""
        for window in clip:
            transcript += window["_source"]['transcript']
            
        episode_uri = window["_source"]["episode_uri"]

        metadata = query_metadata(episode_uri, es)
        metadata = metadata["hits"]["hits"][0]["_source"]

        podcast_clip = {
            "heading": metadata["show_name"] + " - " + metadata["episode_name"],
            "showName": metadata["show_name"],
            "episodeName": metadata["episode_name"],
            "transcript": transcript,
            "startTime": start_time,
            "endTime": end_time
        }

        podcast_clips.append(podcast_clip)

    return podcast_clips

def query_metadata(episode_uri, es):
    # Define the nested query

    query = {
        "query": {
            "match": {
                "episode_uri": episode_uri
            }
        }
    }

    response = es.search(index="episodes", body=query)
    return response

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

def connect_to_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    if not es.indices.exists(index="windows"):
        raise ValueError("Windows index does not exist, run indexer.py")
    
    if not es.indices.exists(index="episodes"):
        raise ValueError("Episodes index does not exist, run indexer.py")
    
    return es

if __name__ == '__main__':
    main()


