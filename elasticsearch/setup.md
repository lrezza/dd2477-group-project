# Elasticsearch setup

Detailed guide in https://github.com/elastic/elasticsearch

## Docker installation

https://www.docker.com/products/docker-desktop

## Install and run elasticsearch through docker
Set up a container with elasticsearch and run it without secure connections (will probably change as the project evolves)
``` bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

## Install elasticsearch for python

Use pip or pip3 below depending on your python installation
``` bash
pip3 install elasticsearch
```

## (OPTIONAL) Install and run kibana through docker
Kibana can be used for viewing the data stored in elasticsearch. The following commands assumes a non-secured http connection to elasticsearch.

``` bash
docker pull docker.elastic.co/kibana/kibana:8.12.2
docker run -d --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```
When kibana is up and running, the UI can be entered through the URL http://localhost:5601
