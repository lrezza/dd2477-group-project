# DD2477 podcast search project

### Installation

#### Docker installation
Download docker desktop
https://www.docker.com/products/docker-desktop

#### Install and run elasticsearch through docker
Set up a container in docker with elasticsearch and run it without secure connections
``` bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

#### Install pip requirements
Use pip or pip3 below depending on your python installation
``` bash
pip3 install -r requirements.txt
```

#### (OPTIONAL) Install and run kibana through docker
Kibana can be used for viewing and debugging the data stored in elasticsearch. The following commands assumes a non-secured http connection to elasticsearch.

``` bash
docker pull docker.elastic.co/kibana/kibana:8.12.2
docker run -d --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```
When kibana is up and running, the UI can be entered through the URL http://localhost:5601

#### Setup the podcast dataset
Download the provided spotify dataset and extract the eight transcript folders labeled 0 to 7 such that they appear in the following way in the root folder of the repository: 

spotify-podcasts-2020/podcasts-transcripts/0 (same for folders 1-7)

Also place the metadata.tsv folder in the spotify-podcasts-2020 folder.

### How to run
Make sure the elasticsearch container is running in docker.

#### Index the podcast dataset
To index the dataset, run the indexer program
(python or python3 depending on your local install, will assume python3)

``` bash
python3 elastic/indexer.py
```

A text-based prompt will appear in the terminal, chose to index episodes and windows. Episodes will only take a couple of minutes, while the indexing of the windows index takes at least one hour. The indexing only has to be done once per index, and the search engine can be run independently of this indexer after the index has been built.

#### Run the search engine
Start reflex in the root of the repository

``` bash
reflex run
```

This starts an instance of the search engine locally (at http://localhost:3000 for me). Enter the URL into your web browser of choice to use the search engine. 