import socks
import socket
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import deque
import random
import time #sleep
import concurrent.futures

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

import logging
# DEBUG < INFO | < WARNING < ERROR < CRITICAL
mylog = logging.getLogger("log")
mylog.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)6s: %(message)s')
stream_hander = logging.StreamHandler()
stream_hander.setLevel(logging.ERROR)
stream_hander.setFormatter(formatter)
file_handler = logging.FileHandler('1106.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
mylog.addHandler(stream_hander)
mylog.addHandler(file_handler)

def page_traverse(seed, tag, visited):
    try:
        curTag = tag.popleft()
        visited.add(curTag)
        url = "http://"+seed+".onion"+tag
        req = requests.get(url, timeout=30)
        soup = BeautifulSoup(req.content, 'lxml')
        with open("./output/"+seed+"/"+seed+".onion"+curTag.replace("/", "#"), 'w') as f:
            f.write(soup.prettify())
        aTag = soup.find_all('a', href=True)
        for h in aTag:
            try:
                at = h['href']
                if at in visited:
                    continue
                if (".onion" in at) or ("http" in at) or ("#" in at) or (at == '/') or (at == ''):
                    continue
                if (".jpg" in at) or (".png" in at):
                    continue
                if (at == '') or (at == '/'):
                    continue
                if at[0] != '/':
                    tag = '/'+tag
                tag.append(at)
            except KeyError: #href 없을 때 
                continue
    except FileNotFoundError:
        mylog.error("FNF "+url)
        return 
    except requests.exceptions.Timeout:
        mylog.error(" TO "+url)
        return 0
    except requests.ConnectionError:
        mylog.error(" CR "+url)
        return 0
    except requests.exceptions.InvalidURL:
        mylog.error(" IU "+url)
        return 0

def worker(seed):
    os.mkdir("output/"+seed) #onion dir 만듬
    mylog.info(seed+" start")
    visitedTag, onionList = set(), deque('')
    onionList.append('')
    visitedTag.add('')
    while onionList:
        time.sleep(random.uniform(3,5))
        page_traverse(seed, onionList, visitedTag)
    mylog.info(seed+" done [result: "+str(len(visitedTag))+"]")
    return

if __name__ == '__main__':  
    if len(sys.argv) != 2:
        sys.exit()
    with open(sys.argv[1].strip(), "r") as f:
        onions = [i.strip() for i in f.readlines()]
    a = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        thread_list = {executor.submit(worker, seed): seed for seed in onions}
    b = time.time()
    mylog.info("total time: "+str(b-a))

# def page_traverse(seed, tag, visited):
#     try:
#         curTag = tag.popleft()
#         visited.append(curTag)
#         url = "http://"+seed+".onion"+tag
#         req = requests.get(url, timeout=30)
#         soup = BeautifulSoup(req.content, 'lxml')
#         save_file(seed, tag, soup.prettify()) #soup 저장
#         aTag = soup.find_all('a', href=True)
#         for h in aTag:
#             try:
#                 at = h['href']
#                 if at in visited:
#                     continue
#                 if (".onion" in at) or ("http" in at) or ("#" in at) or (at == '/') or (at == ''):
#                     continue
#                 if (".jpg" in at) or (".png" in at):
#                     continue
#                 if (at == '') or (at == '/'):
#                     continue
#                 if at[0] != '/':
#                     tag = '/'+tag
#                 tag.append(at)
#             except KeyError: #href 없을 때 
#                 continue
#     except requests.exceptions.Timeout:
#         error("Time out: "+url)
#         return 0
#     except requests.ConnectionError:
#         error("Connection refused: "+url)
#         return 0
#     except requests.exceptions.InvalidURL:
#         error("Invalid URL: "+url)
#         return 0
#test code
# url = "./test/"+seed+"/"+seed+".onion"+curTag
        # with open(url, "r") as f:
        #     soup = BeautifulSoup("".join(f.readlines()))
        #print("visited: %s %s" %(seed, curTag))