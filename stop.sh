#!/bin/bash
sudo kill -9 $(pgrep -f "hypercorn -b 0.0.0.0:8080 main:app") && sudo kill -9 $(sudo netstat -tulnp | awk '/:8080/ {print $7}' | cut -d/ -f1)
