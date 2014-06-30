#!/bin/bash

cat << EOF > /config.json
{
  "network": {
    "servers": [ "$LOGSTASH_PORT_12345_TCP_ADDR:12345" ],
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