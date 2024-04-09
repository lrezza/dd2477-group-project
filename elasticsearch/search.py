from elasticsearch import Elasticsearch

def main():
    es = connect_to_elastic()
    
    #Test queries

    while(True):
        word = input("Type a word to query: ")
        response = query_word(word, es)
        
        """ for hit in response['hits']['hits']:
            print(hit['_source']['episode_uri'])   """

        total_hits = response['hits']['total']['value'] if 'total' in response['hits'] else 0
        print(word, "found in", total_hits, "podcast episodes")


def query_word(word, es):
    # Define the nested query
    max_response_size = 10000
    query = {
        "query": {
            "nested": {
            "path": "windows",
            "query": {
                "nested": {
                "path": "windows.words",
                "query": {
                    "match": {
                    "windows.words.word": word
                    }
                }
                }
            }
            }
        },
        "size": max_response_size
    }

    response = es.search(index="episodes", body=query)
    return response

def connect_to_elastic():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if es.ping():
        print("Connection established to elasticsearch")

    else: 
        raise ValueError("Connection failed")
    
    if not es.indices.exists(index="episodes"):
        raise ValueError("Episode index does not exist, run indexer.py")
    
    return es

if __name__ == '__main__':
    main()