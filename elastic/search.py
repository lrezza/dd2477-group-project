from elasticsearch import Elasticsearch

def main():
    es = connect_to_elastic()
    
    #Test queries

    while(True):
        word = input("Type a word to query: ")
        response = query_episodes(word, es)

        for hit in response["hits"]["hits"]:
            episode_uri = hit["fields"]["episode_uri"][0]
            episode_metadata = query_metadata(episode_uri, es)
            episode_name = episode_metadata["hits"]["hits"][0]["_source"]["episode_name"]
        
            print(episode_name)

def test():
    print("Test called from search.py")
            
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
    
    if not es.indices.exists(index="episodes"):
        raise ValueError("Episodes index does not exist, run indexer.py")
    
    return es

if __name__ == '__main__':
    main()