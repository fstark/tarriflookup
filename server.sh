#!/bin/bash

# Source phython env and starts the server
echo "Starting" >> /tmp/log.txt
cd /Users/fred/Development/tarriflookup/
source venv/bin/activate
echo "Env sourced, starting server" >> /tmp/log.txt
pwd >> /tmp/log.txt
python server.py
echo "Env sourced, server stopped" >> /tmp/log.txt
