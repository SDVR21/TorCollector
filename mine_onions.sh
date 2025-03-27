#!/bin/sh
service tor start
python3 -u mineonions.py ${1:-hack} | tee -a log
