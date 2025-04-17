import socks
import socket
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import deque
import random
import time #sleep
from multiprocessing import Pool
import sys
import os
import io
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from bs4.builder import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
socket.socket = socks.socksocket
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

def error(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)
    return

####### \n 주의
# seed: ~~d xonion
def traverse_all(seed):
    visited, onionList = set(), deque([seed])
    visited.add(seed)
    while onionList:
        now = onionList.popleft()
        if now not in visited:
            visited.add(now)
        if now == seed:
            now = ''
        tl = traverse_list(seed, now)
        time.sleep(random.uniform(1,4))
        if tl == 0:
            continue
        for o in tl:
            if o not in visited:
                onionList.append(o)
    return (len(visited))

def save_file(seed, now, soup):
    now = now.replace("/", "#")
    f = open("./output/"+seed+"/"+seed+".onion"+now, 'w')
    f.write(soup)
    f.close()
    return

def traverse_list(seed, tag):
    try:
        if len(tag) > 0:
            if tag[0] != '/':
                tag = '/'+tag
        url = "http://"+seed+".onion"+tag
        req = requests.get(url, timeout=60)
        soup = BeautifulSoup(req.content, 'lxml')
        save_file(seed, tag, soup.prettify()) #soup 저장
        aTag = soup.find_all('a')
        href_list = []
        key_list = []
        for h in aTag:
            try:
                at = h.attrs['href']
                if ".onion" not in at and "http" not in at and "#" not in at and at != '/':
                    href_list.append(at)
            except KeyError: # a태그인데 href가 없음 
                key_list.append(h)
        href_list = list(set(href_list))
        if len(href_list) == 0:
            if tag == '/': error("no href: "+seed)
            return 0
        return href_list
    except requests.exceptions.Timeout:
        error(f"Timeout encountered for URL: {url}")
        return 0
    except requests.ConnectionError:
        error(f"Connection refused for URL: {url}")
        return 0
    except requests.exceptions.InvalidURL:
        error(f"Invalid URL: {url}")
        return 0

def multi_process(on):
    os.makedirs("output/"+on, exist_ok=True)
    time.sleep(random.uniform(1,4))
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing started for {on}", flush=True)
    vi = traverse_all(on)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing completed for {on} - {vi} items visited", flush=True)
    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("no onion")
        sys.exit()
    a = time.time()
    onions = [o.strip()[:-6] for o in open(sys.argv[1].strip(), "r").readlines()]
    pool = Pool(processes = 4)
    pool.map(multi_process, onions)
    pool.close()
    pool.join()
    b = time.time()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total processing time: {int(b-a)}s", flush=True)
