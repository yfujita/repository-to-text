#!/bin/bash

REPO_PATH=$1
if [ -z "$REPO_PATH" ]; then
    echo "Usage: $0 <path-to-repo> [ignore-dir ...]"
    exit 1
fi
shift

IGNORE_DIRS=""
if [ "$#" -gt 0 ]; then
    IGNORE_DIRS=$(IFS=,; echo "$*")
fi

docker build -t repository-to-text:latest .
docker run --rm -v "$REPO_PATH":/repo:ro -e IGNORE_DIRS="$IGNORE_DIRS" repository-to-text:latest

