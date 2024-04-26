from elasticsearch import Elasticsearch
import math

def main():
    es = connect_to_elastic()

    total_windows = get_total_windows(es)

    while(True):
        query = input("Type a word to query: ")
        words = query.split()
        if len(words) == 1 and words[0] == "quit":
            break

        response = query_episodes(words, es)
        #print(response)
        total_matches = response['hits']['total']['value']
        print(f"Total matches found: {total_matches}")

        # Extract word counts from the aggregation results
        #print(response['aggregations'])
        #word_counts = response['aggregations']['word_counts']['word_count']['buckets']
        #word_count_dict = {word_count['key']: word_count['doc_count'] for word_count in word_counts}

        #for word_count in word_counts:
        #    print(f"Word: {word_count['key']}, Count: {word_count['doc_count']}")

        all_episodes_info = [(entry['fields']['episode_uri'][0], entry['fields']['window_index'][0]) for entry in response['hits']['hits']]
        print(all_episodes_info[0:5])
        
        '''
        Getting the eipisode name and window index

        '''

        # # Compute IDF
        # word_window_frequency = get_window_frequency(es, words)      
        # if word_window_frequency == 0: word_window_frequency = 1e-6
        # idf = math.log(total_windows / word_window_frequency)  # log( N / df )
  
        # # Get all windows containing the queried word
        # all_episodes_info = [(entry['fields']['episode_uri'][0], entry['fields']['window_index'][0]) for entry in response]
       
        # all_result = []
        # # Iterate over each window hit we found and create it's corresponding clip and rank it using tf-idf
        # for i in range(len( all_episodes_info)):
        #   all_result.append(all_episodes(es, all_episodes_info[i][0], all_episodes_info[i][1], idf, word))

        # # Sort the scored clips with the highest scores first
        # sorted_clips = sorted(all_result, key=lambda x: x['tf_idf_score'], reverse=True)

        # # Print the top 10 clips
        # print(sorted_clips[0:10])

'''
The search query
'''
def query_episodes(words, es):

    query = {
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
        },
        # Count the amount of times each word came up across all hits in total
        "aggs": {
            "word_counts": {
                "nested": {
                    "path": "words"
                },
                "aggs": {
                    "word_count": {
                        "terms": {
                            "field": "words.word",
                            "include": words
                        }
                    }
                }
            }
        },
        # Out of all fields in the source, only return these
        "fields": ['episode_uri', 'window_index', 'transcript'],
    }

    response = es.search(index="windows", body=query)
    return response

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


def connect_to_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    #if not es.indices.exists(index="episodes"):
        #raise ValueError("Episode index does not exist, run indexer.py")
    
    return es


def query(episode, window_index):
   query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"episode_uri": episode}},
                         {"terms": {"window_index": window_index}}
                    ]
                }
            }
        }  

   return query  

def calculate_tf_idf(query_word, transcript, idf):
    # Calculate Term Frequency (TF)
    tf = transcript.lower().count(query_word.lower())
    
    # Calculate TF-IDF Score
    tf_idf = tf * idf
    
    return tf_idf
   
def all_episodes(es, episode, window, idf, word):
    '''
    Making 3 windows
    '''

    if(window==0):
     window_index = [window,window+1, window+2]
    else :
     window_index = [window-1,window, window+1]

    response = es.search(index="windows", body=query(episode=episode,window_index=window_index))
    result = {}
    transcripts = ""

    '''
    Mergin the 3 transcripts
    '''
    for i in range(len(response['hits']["hits"])):
        transcripts += response['hits']["hits"][i]['_source']['transcript']

    '''
    The result will be 
    episode_uri
    transcript
    start_time of the first word in the transcript
    end_time of the last word in the transcript
    '''
    result['episode_uri'] = response['hits']["hits"][0]['_source']['episode_uri']
    result['transcript'] = transcripts
    result['start_time'] = response['hits']["hits"][0]['_source']['words'][0]['start_time']
    result['end_time'] = response['hits']["hits"][-1]['_source']['words'][-1]['end_time']

    tf_idf_score = calculate_tf_idf(word, transcripts, idf)
    
    # Construct the result with the TF-IDF score
    result['tf_idf_score'] = tf_idf_score
    
    return result   


if __name__ == '__main__':
    main()