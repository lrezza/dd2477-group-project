from elasticsearch import Elasticsearch

def main():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if not es.ping():
        raise ValueError("Connection failed")



if __name__ == '__main__':
    main()