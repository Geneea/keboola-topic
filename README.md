# Geneea topic detection API demo

A simple example of using topic detection with Geneea API which can be integrated with Keboola.
It's implemented as a Docker container with a python script calling the Geneea API.

## Building a container

```
git clone https://github.com/Geneea/keboola-topic.git
cd keboola-topic
sudo docker build --no-cache -t geneea/keboola-topic .
```

## Running a container

```
sudo docker run \
--volume=/home/ec2-user/data:/data \
--rm \
geneea/keboola-topic:latest
```
Note: `--volume` needs to be adjusted accordingly.

## Sample configuration
Mapped to `/data/config.yml`

```
storage:
  input:
    tables:
      0:
        source: source.csv
  output:
    tables:
      0:
        source: topic.csv
parameters:
  primary_key_column: id
  data_column: text
  user_key: <ENTER YOUR API KEY HERE>
```

## Sample data

### Input
Read from `/data/in/tables/source.csv`

```
id,text
1,"He won gold and silver medals at the past two Olympic Games, and even has an aquatic arena named after him."
2,"The museum was considered to host one of the world's greatest archaeological collections."
3,"These measurements should allow us to confirm some of the basic features of the greenhouse effect."
```

### Output
Written to `/data/out/tables/topic.csv`

```
id,topic,confidence
1,Sports,0.467843459155
2,Science,0.373045280015
3,Other,NaN
```
