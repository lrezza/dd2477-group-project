from elasticsearch import Elasticsearch

def main():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the connection is successful
    if not es.ping():
        raise ValueError("Connection failed")

    # Create index
    #es.indices.create(index="some_index")

    # Add documents to index
    es.index(
        index="some_index",
        id="doc1",
        document={
            "first_name": "John",
            "last_name": "Doe",
        }
    )

    es.index(
        index="some_index",
        id="doc2",
        document={
            "first_name": "Mr",
            "last_name": "Bean",
        }
    )

    es.index(
        index="some_index",
        id="doc3",
        document={
            "first_name": "Jack",
            "last_name": "Daniels",
        }
    )

    # Find a specific document in index
    result = es.get(index="some_index", id="doc1")
    print(result)

    # Query for documents in index
    result = es.search(index="some_index", query={
        "match": {
            "first_name": "John"
        }
    })
    print(result)

if __name__ == '__main__':
    main()