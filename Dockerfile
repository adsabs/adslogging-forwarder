
#
# logstash-forwarder Dockerfile
# inspiration: https://github.com/denibertovic/logstash-forwarder-dockerfile
#
 
# Pull base image.
FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update

# install deps
RUN apt-get install -y wget git golang ruby ruby-dev irb ri rdoc build-essential libopenssl-ruby1.9.1 libssl-dev zlib1g-dev

# clone logstash-forwarder
RUN git clone git://github.com/elasticsearch/logstash-forwarder.git /tmp/logstash-forwarder
RUN cd /tmp/logstash-forwarder && go build

# Install fpm
RUN gem install fpm

# Build deb
RUN cd /tmp/logstash-forwarder && make deb
RUN dpkg -i /tmp/logstash-forwarder/logstash-forwarder_*_amd64.deb

# Cleanup
RUN rm -rf /tmp/*

ADD run.sh /run.sh
RUN chmod 755 /run.sh

CMD /run.sh
