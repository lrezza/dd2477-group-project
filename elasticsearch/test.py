from elasticsearch import Elasticsearch

def main():
    es = connect_to_elastic()
    
   

    while(True):
        word = input("Type a word to query: ")
        if word == "quit":
           break
        response = query_episodes(word, es)
        
        '''
        Getting the eipisode name and window index

        '''
        
        all_episodes_info = [(entry['fields']['episode_uri'][0], entry['fields']['window_index'][0]) for entry in response['hits']["hits"]]

        all_result = []
        #using thefunction all_episodes to get the n-clip
        for i in range(len( all_episodes_info)):
          all_result.append(all_episodes( all_episodes_info[i][0], all_episodes_info[i][1], es))
        # Assuming 'response' is the result of your Elasticsearch query
        total_matches = response['hits']['total']['value']
        print(f"Total matches found: {total_matches}")

        #print(all_result) 
        #return all_result





'''
The seacrh query
'''
def query_episodes(word, es):
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
        "size": 1000000,

        "fields": ['episode_uri', 'window_index', 'transcript'],
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
   
def all_episodes(episode, window, es):
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
    
    return result   


if __name__ == '__main__':
    main()