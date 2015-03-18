FROM keboola/base
MAINTAINER Tomáš Mudruňka <mudrunka@geneea.com>

# setup the environment
WORKDIR /tmp
RUN yum -y install wget git
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install requests
RUN pip install PyYaml

# prepare the container
WORKDIR /home
RUN git clone https://github.com/Geneea/keboola-topic.git ./

ENTRYPOINT python ./src/topic.py --data=/data
