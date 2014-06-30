#!/bin/bash

cat << EOF > /config.json
{
  "network": {
    "servers": [ "$LOGSTASH_PORT_12345_TCP_ADDR:12345" ],
	"ssl certificate": "/opt/certs/forwarder.crt",
    "ssl key": "/opt/certs/forwarder.key",
    "ssl ca": "/opt/certs/forwarder.crt",
    "timeout": 15
  },
  "files": [
    {
      "paths": [ "/dev/log" ],
      "fields": { "type": "syslog" }
    }
  ]
}
EOF

/opt/logstash-forwarder/bin/logstash-forwarder -config /config.json