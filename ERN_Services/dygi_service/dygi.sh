#!/bin/bash

cd /app

/usr/local/bin/python3.7 news_handler/main.py

if ! pgrep -f "allennlpPredict.py"

then

file=news_handler/docs.jsonl
minimumsize=1
actualsize=$(wc -c <"$file")

if [ $actualsize -ge $minimumsize ];

then

/usr/local/bin/python3.7 allennlpPredict.py

else

echo size is under $minimumsize byte

fi

find /tmp/. -type d -exec rm -rf {} +

fi