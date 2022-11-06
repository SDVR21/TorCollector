import socks
import socket
import requests
from bs4 import BeautifulSoup
from collections import deque
import random
import time #sleep
from multiprocessing import Pool
import os

import sys
import io
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

def error(errtag, str):
    print(errtag, ":", str)
    return

def page_traverse(seed, tag, visited):
    try:
        url = "http://"+seed+".onion"+tag
        req = requests.get(url, timeout=30)
        soup = BeautifulSoup(req.content, 'lxml')
        with open("./output/"+seed+"/"+seed+".onion"+tag.replace("/", "#"), 'w') as f:
            f.write(soup.prettify())
        aTag = soup.find_all('a', href=True)
        href_list = []
        for h in aTag:
            at = h['href']
            if (".onion" in at) or ("http" in at) or ("#" in at) or (at == '/') or (at == ''):
                continue
            if (".jpg" in at) or (".png" in at):
                continue
            if at[0] != '/':
                tag = '/' + tag
            if at in visited:
                continue
            href_list.append(at)
        return href_list
    except requests.exceptions.Timeout:
        error("TO", url)
        return 0
    except requests.ConnectionError:
        error("CR", url)
        return 0
    except requests.exceptions.InvalidURL:
        error("IU", url)
        return 0

def traverse_all(seed):
    os.mkdir("output/"+seed)
    print("[", seed, "] start")
    visitedTag, onionList = set(), deque()
    onionList.append('')
    visitedTag.add('')
    while onionList:
        now = onionList.popleft()
        visitedTag.add(now)
        time.sleep(random.uniform(3,5))
        tmp = page_traverse(seed, now, visitedTag)
        if tmp:
            onionList.extend(tmp)
    print("[", seed, "] done - result: ", len(visitedTag))
    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("python3 page_traverse.py onion.txt")
        sys.exit()
    with open(sys.argv[1].strip(), "r") as f:
        onions = [i.strip()[:-6] for i in f.readlines()]
    pool = Pool(processes = 4)
    pool.map(traverse_all, onions)
    pool.close()
    pool.join()
