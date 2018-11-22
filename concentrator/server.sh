#! /bin/bash

echo "$CONFIG" > config.json
twistd -n -y /server.py
