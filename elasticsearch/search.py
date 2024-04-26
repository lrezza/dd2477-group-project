from elasticsearch import Elasticsearch
import math

def main():
    es = connect_to_elastic()
    
    total_windows = get_total_windows(es)
    print(f"Total number of windows: {total_windows}")

    while(True):
        query = input("Type a word to query: ")
        words = query.split()
        if len(words) == 1 and words[0] == "quit":
            break
        
        # retrieves up to 50 windows from the index that elasticsearch deems are most relevant
        top_relevant_windows = get_windows_with_all_words(es, words)
        print(f"Relevant windows containing all words: {len(top_relevant_windows)}")
        print(top_relevant_windows[0:5])
        # Use this to then create clips
        
        if top_relevant_windows == 0: 
            print(f"No podcast contains all inputted keywords")
            # Should we break or return a list that's relevant based on the words in the query that is in index? 

        print()
        for word in words:
            word_window_frequency = get_window_frequency(es, word)
            if word_window_frequency == 0: word_window_frequency = 1e-6
            idf = math.log(total_windows / word_window_frequency)  # log( N / df )

            print(f"Word - {word} \n\t\tWindow_frequency: {word_window_frequency}\n\t\tIDF: {idf}")
        print()

def get_windows_with_all_words(es, words):
    # Construct the query
    query = {
        "size": 50,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "words",
                            "query": {
                                "match": {
                                    "words.word": word
                                }
                            }
                        }
                    } for word in words
                ]
            }
        }
    }
    # Execute the query
    response = es.search(index="windows", body=query)

    # Extract the window indices
    windows = []
    for hit in response['hits']['hits']:
        window_index = hit['_source']['window_index']
        episode_uri = hit['_source']['episode_uri']
        windows.append((window_index, episode_uri))
    return windows

def get_total_windows(es):
    # Formulate query
    query = {
        "query": {"match_all": {}},
        "aggs": {
                "total_windows": {
                    "value_count": {
                        "field": "window_index"
                    }
                }
            },
        "size": 0
        }
    # Run query
    response = es.search(index="windows", body=query)

    # Extract the total count from the response
    return response['aggregations']['total_windows']['value']

def get_window_frequency(es, word):
    # Formulate query
    query = {
        # We want to find all windows containing the specified word, and each window has it's corresponding word list
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
        # We specify that we don't care about the actual returned results of the query
        "size": 0,
        # We want count the total amount of windows we have matched with, so we count the amount of window_indexes we matched with
        "aggs": {
                "window_frequency": {
                    "value_count": {
                        "field": "window_index"
                    }
                }
            },
        }
    # Run query
    response = es.search(index="windows", body=query)

    # Extract the total count from the response
    return response['aggregations']['window_frequency']['value']

def query_episodes(word, es):
    # Define the nested query
    max_response_size = 10000

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
    
    return es

if __name__ == '__main__':
    main()


