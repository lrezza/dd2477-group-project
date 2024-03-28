from elasticsearch import Elasticsearch

def main():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if not es.ping():
        raise ValueError("Connection failed")

    # Create an index
    es.indices.create(index="my-test-index", ignore=400)

    # Index some document
    es.index(index="my-test-index", id=1, document={"text": "Elasticsearch in Docker"})

    # Retrieve the document
    doc = es.get(index="my-test-index", id=1)
    print(doc)

    # Search for documents
    search_result = es.search(index="my-test-index", query={"match_all": {}})
    print(search_result)


if __name__ == '__main__':
    main()