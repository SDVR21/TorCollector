#!/bin/sh
service tor start
python3 run_multiprocess.py onion.txt | tee -a log
tail -f /dev/null
