#!/bin/bash
ES_HOME=/usr/share/elasticsearch
ES_PATH_CONF=/etc/elasticsearch


mkdir tmp
mkdir tmp/cert_blog

sudo echo "127.0.0.1 kibana.local logstash.local" >> /etc/hosts
sudo echo "127.0.0.1 $1" >> /etc/hosts

sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert ca --pem --in ~/tmp/cert_blog/instance.yml --out ~/tmp/cert_blog/certs.zip

cp configs/elasticsearch.yml /etc/elasticsearch.yml

cd ~/tmp/cert_blog/
unzip certs.zip
cd $ES_PATH_CONF
mkdir certs
cp ~/tmp/cert_blog/certs/ca/ca.crt ~/tmp/cert_blog/certs/$1/* certs
nohup /usr/share/elasticsearch/bin/elasticsearch > /dev/null &
sleep 15
cd $ES_HOME
bin/elasticsearch-setup-passwords auto -u


KIBANA_HOME=/usr/share/kibana
KIBANA_PATH_CONFIG=/etc/kibana

cd $KIBANA_PATH_CONFIG
mkdir certs
cp ~/tmp/cert_blog/certs/ca/ca.crt ~/tmp/cert_blog/certs/$1/* certs
sudo cp configs/kibana.yml /etc/kibana/kibana.yml

sudo service kibana start
