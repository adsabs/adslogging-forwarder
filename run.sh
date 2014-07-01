#!/bin/bash

logstash_server=${LOGSTASH_SERVER-localhost:12345}

cat << EOF > /config.json
{
  "network": {
    "servers": [ "$logstash_server" ],
	"ssl certificate": "/opt/certs/forwarder.crt",
    "ssl key": "/opt/certs/forwarder.key",
    "ssl ca": "/opt/certs/forwarder.crt",
    "timeout": 15
  },
  "files": [
    {
      "paths": [ "/var/log/syslog" ],
      "fields": { "type": "syslog" }
    }
  ]
}
EOF

/opt/logstash-forwarder/bin/logstash-forwarder -config /config.json