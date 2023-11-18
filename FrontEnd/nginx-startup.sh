#!/bin/bash

echo "Starting application..."
echo "replace API_URL in runtime.json or update it if it already exists"
echo "API_URL = ${API_URL}"

if grep -q "$API_URL" /usr/share/nginx/html/assets/json/runtime.json; then
    envsubst < /usr/share/nginx/html/assets/json/runtime.json > /tmp/runtime.json
    cp /usr/share/nginx/html/assets/json/runtime.json /tmp/runtime.json.bak
    cp /tmp/runtime.json /usr/share/nginx/html/assets/json/runtime.json
    rm /tmp/runtime.json

else
    cp /tmp/runtime.json.bak /usr/share/nginx/html/assets/json/runtime.json
    envsubst < /usr/share/nginx/html/assets/json/runtime.json > /tmp/runtime.json
    cp /tmp/runtime.json /usr/share/nginx/html/assets/json/runtime.json
    rm /tmp/runtime.json
fi

nginx -g 'daemon off;'