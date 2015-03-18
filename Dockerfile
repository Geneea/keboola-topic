FROM keboola/base
MAINTAINER Tomas Mudrunka <mudrunka@geneea.com>

RUN git clone https://github.com/Geneea/keboola-topic.git ./

ENTRYPOINT python ./src/topic.py --data=/data
