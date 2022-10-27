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

def error(str):
    print(str)
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
        time.sleep(random.uniform(3,5))
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
        req = requests.get(url)
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
    except requests.ConnectionError:
        error("Connection refused: "+url)
        return 0
    except requests.exceptions.InvalidURL:
        error("Invalid URL: "+url)
        return 0

def multi_processsss(on):
    os.mkdir("output/"+on)
    time.sleep(random.uniform(3,5))
    print("********** ", on, " start **********")
    vi = traverse_all(on)
    print("********** %s done ********** (result: %d)" %(on, vi))
    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("no onion")
        sys.exit()
    a = time.time()
    onions = [o.strip()[:-6] for o in open(sys.argv[1].strip(), "r").readlines()]
    pool = Pool(processes = 4) # 4개의 프로세스를 사용합니다.
    pool.map(multi_processsss, onions)
    pool.close()
    pool.join()
    b = time.time()
    print("----------------------- total: ", b-a,"s")
