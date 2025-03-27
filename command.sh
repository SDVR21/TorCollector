#!/bin/sh
service tor start
python3 -u run_multiprocess.py onion.txt | tee -a log
