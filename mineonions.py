import socks
import socket
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter
from collections import deque
import random
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from bs4.builder import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

from datetime import datetime
import time
import collections
import re
#'[13][A-HJ-NP-Za-km-z1-9]{25,33}|[a-z1-9]{55}d\.onion|[a-z1-9]{16}\.onion'
onion_rex=re.compile("[a-z1-9]{55}d\.onion") 

socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
socket.socket = socks.socksocket
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

def my_request(onion):
    try:
        req = requests.get("http://"+onion, timeout=30)
        soup = BeautifulSoup(req.content, 'lxml')
        return (soup)
    except requests.ConnectionError:
        #print("Connection refused ", onion)
        return (-1)
    except requests.exceptions.InvalidURL:
        #print("Invalid URL ", onion)
        return (-1)
    except requests.exceptions.ReadTimeout:
        return (-1)
        
def save_file(onion, now, soup):
    f = open(onion+"/"+now+".txt", 'w')
    f.write(soup)
    f.close()
    return


def page_traverse(onion):
    soup = my_request(onion+".onion")
    save_file(onion, onion+".onion", soup)
    if soup == -1:
        return (-1)
    href = soup.find_all('a')
    href_list = []
    for h in href:
        at = h.attrs['href']
        if ".onion" not in at and "http" not in at:
            href_list.append(at)
    for hr in href_list:
        hr_soup = my_request(onion+".onion"+hr)
        if hr_soup != -1:
            print(hr)

def onion_list(onion, re):
    try:
        with requests.get("http://"+onion, timeout=10) as req:
            soup = BeautifulSoup(req.content, 'lxml')
        ma=onion_rex.findall(soup.text)
        if ma:
            if ma[0]==onion:
                pass
                #print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collected {len(ma)} urls from onion", flush=True)
            # print("**********************%d", len(ma))
            return set(ma)
        else:
            return 0
    except requests.ConnectionError:
        # print("Connection refused")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connection refused: {onion}", flush=True)
        return 0
    except requests.exceptions.InvalidURL:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Invalid URL: {onion}", flush=True)
        # print("Invalid URL")
        return 0
    except requests.exceptions.ReadTimeout:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connection timeout: {onion}", flush=True)
        return 0
    # no_result = soup.find('p')
    # if no_result!=None:
    #     print(no_result.text+"\n")
    #     return

def bfs(onion, key):
    count=0
    f1 = open(key+".txt", 'w', encoding='utf-8')
    oset = set()
    visited, queue = set(), collections.deque([onion])
    visited.add(onion)
    while queue:
        # Dequeue a vertex from queue
        vertex = queue.popleft()
        f1.write(vertex+"\n")
        count+=1
        if vertex not in visited:
            visited.add(vertex)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Visited: {vertex}", flush=True)

        # If not visited, mark it as visited, and
        # enqueue it
        s = onion_list(vertex, 0)
        if s==0:
           continue
        for o in s:
           queue.append(o)
           
        time.sleep(random.uniform(1,4))
        
    f1.write("********************** visited: "+str(len(visited))+"  count: "+str(count)+"\n")
    f1.close()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ********************** visited: {str(len(visited))}  count: {str(count)}", flush=True)
    return



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("python3 mineonions.py [keyword]")
        sys.exit()
    keyword = sys.argv[1].strip()
    # https://ahmia.fi/search/?q=asdkljfsd
    onion="ahmia.fi/search/?q="+keyword
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting from keyword {keyword}: {onion}", flush=True)
    bfs(onion, keyword)
