#!/bin/bash
supervisord -c <(envsubst < /etc/supervisord.conf)