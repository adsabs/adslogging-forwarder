#!/bin/bash

cat << EOF > /config.json
{
  "network": {
    "servers": [ "$LOGSTASH_SERVER" ],
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