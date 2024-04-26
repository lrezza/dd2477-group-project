from elasticsearch import Elasticsearch
import math

"""
Episode: 1je9ZwsTlHyWFfiKylvo6V   Window: 29
 This is an event in the Star Wars Galaxy.

Episode: 1je9ZwsTlHyWFfiKylvo6V   Window: 30
 That not only had consequences that the entire galaxy felt. It was Galaxy shattering Not only was this in essence the second Jedi Purge.

Episode: 1je9ZwsTlHyWFfiKylvo6V   Window: 31
 Not only was this the event that broke Luke Skywalker Luke Skywalker that broke him into making him run and go into hiding this is the turn of another member of the Skywalker bloodline to the dark side. 
 This is a huge event in the Star Wars Galaxy. This is huge for the Star Wars saga. This is a story that is if told correctly

Episode: 2usKBOABZO5oPM4XFcqeQ1   Window: 39
 My favorite ride. Alright, so we go I'm gonna Indiana Jones All rights Pirates.

Episode: 2usKBOABZO5oPM4XFcqeQ1   Window: 40
 The Guardians of the Galaxy during the Galaxy was fun, you know, the guy that was talking to us from Guardians of the Galaxy.

Episode: 2usKBOABZO5oPM4XFcqeQ1   Window: 41
 Remember he was like he was another one of those guys that just want to have conversation. He's like, you know, they play a different song every time you drop your mind you the guy came just like I was a distant as I probably wasn't as racist.
 Well, that's what I'm saying is that's what he was a digit. He was like the PG version of that other guy. Yeah, like I just thought like that other guy case want to talk just like how this guy wanted to tell us about how every time there's a different song The Guardians of the Galaxy. There's different triple drops drop sequence. Yeah. That's kind of funny though, right remember that.
"""


def main():
    es = connect_to_elastic()

    # Define the episode URI and window indices
    while(True):
        query = input("Type a word to query: ")

        if query == "quit":
            break

        # Split the input into an array of words
        query_words = query.split()

        # Get top 20 windows based on their transcript scores
        search_result = search_windows_by_transcript(es, query_words)

        # Print scores to double check if scores ordering is correct
        print(f"Total Scores: {len(search_result['hits']['hits'])}")
        print("Scores:")
        for hit in search_result['hits']['hits']:
            formatted_hit_score = "{:.8f}".format(hit["_score"])
            print(formatted_hit_score)

        # Print first 5 transcripts to double check if scores are reasonable
        print("First 5 Results:")
        for hit in search_result['hits']['hits'][:5]:
            print(hit["_source"]['transcript'])  
            print()

        # Combine the ranked windows into clips
        clips = create_clips_from_hits(es, search_result['hits']['hits'])

        # Print first 5 clip transcripts to double clips are correct
        print("First 5 Results in created clips:")
        for clip in clips[:5]:
            for window in clip:    
                print(window["_source"]['transcript'])  
            print()

        # Aggregate scores for each clip
        clips_with_scores = [(clip, sum(window['_score'] for window in clip)) for clip in clips]

        # Rank clips based on aggregated scores
        ranked_clips = sorted(clips_with_scores, key=lambda x: x[1], reverse=True)

        # Print the top 5 ranked clips
        print("Top 5 Ranked Clips:")
        for rank, (clip, score) in enumerate(ranked_clips[:5], start=1):
            print(f"Rank {rank}: Score {score}")
            for window in clip:
                print(window["_source"]['transcript'])
            print()
        
    
def search_windows_by_transcript(es, query_words):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"transcript": word}} for word in query_words
                ]
                # ,"minimum_should_match": (len(query_words) // 2) + 1
            }
        },
        "sort": [{
                "_score": {
                    "order": "desc"
                }
            }
        ],
        "size": 100
    }

    # Execute the query
    result = es.search(index="windows", body=query)
    return result

def create_clips_from_hits(es, hits):
    # Initialize an empty list to store clips
    clips = []

    # Iterate over the hits to combine them into clips
    for hit in hits:
        # Extract the window index from the hit
        window_index = hit["_source"]["window_index"]
        episode_uri = hit["_source"]["episode_uri"]
        #print(f"window_index: {window_index}")
        #print(f"epsidode_uri: {episode_uri}")
        
        # Find the indices of the adjacent windows
        left_index = window_index - 1
        right_index = window_index + 1

        # Retrieve the adjacent windows from the hits list
        left_window = get_window_by_index_and_ep(es, episode_uri, left_index)
        right_window = get_window_by_index_and_ep(es, episode_uri, right_index)

        # window_index: 30
        # epsidode_uri: 1je9ZwsTlHyWFfiKylvo6V
        # left_window:  'episode_uri': '1je9ZwsTlHyWFfiKylvo6V', 'window_index': 29,
        # right_window: 'episode_uri': '1je9ZwsTlHyWFfiKylvo6V', 'window_index': 31

        # window_index: 13
        # epsidode_uri: 2nfi9fT9nHHmcL2rm5yWqN
        # left_window:  'episode_uri': '2nfi9fT9nHHmcL2rm5yWqN', 'window_index': 12,
        # right_window: episode_uri': '2nfi9fT9nHHmcL2rm5yWqN', 'window_index': 14

        # seems to work

        # If both adjacent windows exist, create clip as per usual
        if left_window is not None and right_window is not None:
            clip = [left_window, hit, right_window]
            print("Transcript for current clip:")
            print(f"Episode: {left_window['_source']['episode_uri']}   Window: {left_window['_source']['window_index']} \nEpisode: {hit['_source']['episode_uri']}   Window: {hit['_source']['window_index']}\nEpisode: {right_window['_source']['episode_uri']}   Window: {right_window['_source']['window_index']}")
            print(f"{left_window['_source']['transcript']} \n{hit['_source']['transcript']} \n{right_window['_source']['transcript']}")
            print()
        # If left_window or right_window is None, handle the edge case

        # If left_window is None
        elif left_window is None:
            second_right_window = get_window_by_index_and_ep(es, episode_uri, right_index + 1)
            clip = [hit, right_window, second_right_window]

        # If right_window is None
        else:
            second_left_window = get_window_by_index_and_ep(es, episode_uri, left_index - 1)
            clip = [second_left_window, left_window, hit]

        # Add the clip to the list of clips
        clips.append(clip)

    return clips

def get_window_by_index_and_ep(es, episode_url, window_index):
    # Define the query to retrieve the window by its index and episode URL
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"episode_uri": episode_url}},
                    {"match": {"window_index": window_index}}
                ]
            }
        }
    }

    # Execute the query
    result = es.search(index="windows", body=query)

    # Extract and return the window from the search result
    if result["hits"]["total"]["value"] > 0:
        return result["hits"]["hits"][0]
    else:
        return None

def connect_to_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    return es

if __name__ == '__main__':
    main()