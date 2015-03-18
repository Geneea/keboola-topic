FROM keboola/base
MAINTAINER Tomas Mudrunka <mudrunka@geneea.com>

# initialize the environment
WORKDIR /home
RUN yum -y install git
RUN git clone https://github.com/Geneea/keboola-topic.git ./

ENTRYPOINT python ./src/topic.py --data=/data
