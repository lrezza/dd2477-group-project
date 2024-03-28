# Elasticsearch setup

Detailed guide in https://github.com/elastic/elasticsearch

## Docker installation

https://www.docker.com/products/docker-desktop

## Install and run elasticsearch through docker
``` bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

Save the generated password and enrollment token for kibana. Since outputs are printed to the terminal, these may get lost. Can be found again in docker application if you can not scroll up far enough in the terminal. 

## Install and run kibana through docker

``` bash
docker pull docker.elastic.co/kibana/kibana:8.12.2
docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```

Enter the generated unique URL (again this also can be lost if you wait a while, should be findable in docker application)

Paste the enrollment token from the elasticsearch setup, and login with the username 'elastic, and password from the elasticsearch setup.

## Install elasticsearch for python

Use pip or pip3 below depending on your python installation
``` bash
pip3 install elasticsearch
```
