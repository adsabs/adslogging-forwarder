adslogging-forwarder
====================

logstash-forwarder container

## Requirements

* git, python, openssl
* [docker](http://docker.io), preferably >= v1.0
* [fabric](http://www.fabfile.org/)

## SSL Certificates

Communication between the logstash-forwarder agent and logstash requires the use of ssl certificates. The path to these certificates must be configured in both the input configuration of your logstash instance (logstash.conf) and in the config.js of logstash-forwarder.

The [Dockerfile](Dockerfile) expects these certificate files to be in `./certs` and will add this directory to the container with the target path of `/opt/certs`.

To generate a set of certificate files you can use the provided fabric command, `fab gen_certs`. You'll then need to get these certificates into your logstash container as well. Note that the Dockerfile ADD operation does not follow symlinks. :cry:

## Install & Setup

1. `git clone https://github.com/adsabs/adslogging-forwarder.git`
1. `cd adslogging-forwarder`
1. `fab gen_certs` or otherwise get your ssl certificate files into ./certs
1. `fab build` to build the docker image

## Running

The default entrypoint for the container is the [run.sh](run.sh) script which writes out the logstash-forwarder configuration to config.js and then executes the agent. By default the forwarder will try to attach to `localhost:12345`. 

To run the container: `fab run`

To run the container with an alternate entrypoint: e.g., `fab run:ep=bash`

### setting $LOGSTASH_SERVER

The config.js template anticipates a `$LOGSTASH_SERVER` env variable which should be set to the hostname/ip of the logstash instance, including the port that the logstash [lumberjack](http://logstash.net/docs/1.4.2/inputs/lumberjack) input filter is configured to listen on. 

To run the container specifying the logstash server: e.g., `fab run:LOGSTASH_SERVER=myhost:3331`