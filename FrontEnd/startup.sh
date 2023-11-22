#!/bin/bash
envsubst < /etc/supervisord.conf > /tmp/supervisord.conf
supervisord -c /tmp/supervisord.conf