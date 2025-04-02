import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
import re
btcrex=re.compile("[13][A-HJ-NP-Za-km-z1-9]{26,33}")
segrex=re.compile("bc1[ac-hj-np-z02-9]{39,59}") #bc1[ac-hj-np-z02-9]39,59
base32="023456789acdefghjklmnpqrstuvwxyz"

# def validate(bitcoin):
#     result = os.popen('php validate.php '+bitcoin).read()
#     if result == 'yes':
#         return (1)
#     if result == 'no':
#         return (0)
#     return (0)

import hashlib
import binascii

def check_address(address: str) -> bool:
    orig_base58 = address
    dec = 0
    base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for ch in address:
        try:
            dec = dec * 58 + base58_alphabet.index(ch)
        except ValueError:
            return False
    new_address = ""
    hex_digits = "0123456789ABCDEF"
    while dec > 0:
        dv = dec // 16
        rem = dec % 16
        dec = dv
        new_address += hex_digits[rem]
    new_address = new_address[::-1]
    for ch in orig_base58:
        if ch == '1':
            new_address = "00" + new_address
        else:
            break
    if len(new_address) % 2 != 0:
        new_address = "0" + new_address
    if len(new_address) != 50:
        return False
    if int(new_address[:2], 16) > 0:
        return False
    try:
        payload = binascii.unhexlify(new_address[:-8])
    except binascii.Error:
        return False
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).hexdigest().upper()[:8]
    return checksum == new_address[-8:]

def scan_bitcoin_addresses(path):
    btc_list = []
    seg_list = []
    with open(path, 'r') as f:
        text = f.read()
    ma1=btcrex.findall(text)
    ma2=segrex.findall(text)
    if ma1:
        btc_list += [m for m in ma1 if m not in path and check_address(m)]
    if ma2:
        seg_list += [m for m in ma2]
    return (set(btc_list), set(seg_list))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract_bitcoin.py [file_or_directory]")
        sys.exit(1)

    target = sys.argv[1]
    onion = target.split("/")[-1]
    if os.path.isfile(target):
        btc_list, seg_list = scan_bitcoin_addresses(target)
        print(f"BTC addresses: {len(btc_list)}, Segwit addresses: {len(seg_list)}")
        for btc in btc_list:
            print(btc)
        for seg in seg_list:
            print(seg)
    elif os.path.isdir(target):
        btc_list = set()
        seg_list = set()
        page_list = os.listdir(target)
        for page in page_list:
            if onion not in page:
                continue
            btc_tmp, seg_tmp = scan_bitcoin_addresses(target + "/" + page)
            btc_list.update(btc_tmp)
            seg_list.update(seg_tmp)
        print(f"BTC addresses: {len(btc_list)}, Segwit addresses: {len(seg_list)}")
        with open("bitaddr_"+onion+".txt", 'w') as f:
            f.write(f"BTC addresses: {len(btc_list)}, Segwit addresses: {len(seg_list)}")
            f.write("\n")
            f.write("\n".join(btc_list))
            f.write("\n")
            f.write("\n".join(seg_list))
    else:
        print("Invalid path")
