#!/bin/sh
service tor start
python3 page_traverse.py onion.txt | tee -a log
tail -f /dev/null