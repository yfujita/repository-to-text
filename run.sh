#!/bin/bash

REPO_PATH=$1
if [ -z "$REPO_PATH" ]; then
    echo "Usage: $0 <path-to-repo>"
    exit 1
fi

docker rm repository-to-text:latest
docker build -t repository-to-text:latest .
docker run -v $REPO_PATH:/repo repository-to-text:latest

