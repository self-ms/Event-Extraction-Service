#!/bin/bash

crontab -r

cat /app/dygi_service.env > /etc/environment

echo "*/15 * * * * /app/dygi.sh >> /app/crontab_log 2>&1" | crontab -

cpulimit --path /usr/local/bin/python3.7 --limit 600 --background