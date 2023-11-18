#!/bin/bash

# URL to check
url="http://localhost:8080/health"

# Execute curl, hide output, fail on error and save response
response=$(curl --silent --fail "$url")

# Verify if response contains "ok":true
if echo "$response" | grep -q '{"ok":true}'; thens
    echo "Health check passed."
    exit 0
else
    echo "Health check failed."
    exit 1
fi