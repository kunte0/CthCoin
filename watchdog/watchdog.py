#!/usr/bin/env python3
import json
from binascii import hexlify, unhexlify
from ecdsa import NIST384p, util
import requests as r
from os import urandom
from sys import argv
from bs4 import BeautifulSoup


THE_FLAG = 'flag{mT_g0x_?;_;!_wh3erE_iS_Our__Mon..EY_\//\}'

# getto parser
if len(argv) != 3:
    exit(1)


IP = argv[1]
PORT = argv[2]
URL = IP + ':' + PORT

if 'http' not in URL:
    URL = 'http://' + URL


def register(username, password):
    register_data = {
        'username': 'hash',
        'password': 'hash',
        'confirm': 'hash'
    }
    register_data['username'] = username
    register_data['password'] = password
    register_data['confirm'] = password

    r.post(URL + '/register', data=register_data)


def login(username, password):
    login_data = {
        'username': 'hash',
        'password': 'hash',
    }
    login_data['username'] = username
    login_data['password'] = password

    login = r.post(URL + '/login', data=login_data)

    return login.cookies


def get_coins(session):
    wallet = r.get(URL + '/wallet', cookies=session)
    soup = BeautifulSoup(wallet.text, 'html.parser')
    coins = soup.find_all(id='coin')
    return coins


def buy_flag(session, coins):
    buy_data = {}
    buy_data['coin'] = coins[1].string
    r.post(URL + '/buy/2', cookies=session, data=buy_data)
    buy_data['coin'] = double_spend(coins[1].string)
    r.post(URL + '/buy/2', cookies=session, data=buy_data)
    buy_data['coin'] = coins[2].string
    r.post(URL + '/buy/2', cookies=session, data=buy_data)
    buy_data['coin'] = double_spend(coins[2].string)
    flag = r.post(URL + '/buy/2', cookies=session, data=buy_data)
    soup = BeautifulSoup(flag.text, 'html.parser')
    flag = soup.find(id='flag')
    return flag.string


def double_spend(coin):
    data = json.loads(coin)
    sig = unhexlify(data['SIG'])
    r, s = util.sigdecode_string(sig, NIST384p.order)
    # this is it
    sig2 = util.sigencode_string(r, NIST384p.order - s, NIST384p.order)
    coin = {}
    coin['MN'] = 'F9BEB4E1'
    coin['NC'] = data['NC']
    coin['AM'] = data['AM']
    coin['TS'] = data['TS']
    coin['OW'] = data['OW']
    coin['CU'] = 'NIST384'
    coin['PK'] = data['PK']
    coin['SIG'] = hexlify(sig2).decode('utf-8')
    return json.dumps(coin, sort_keys=True)


def main():
    username = hexlify(urandom(16))[:25]
    password = hexlify(urandom(16))

    try:
        register(username, password)
        session = login(username, password)
        coins = get_coins(session)
        if len(coins) != 3:
            exit(1)
        flag = buy_flag(session, coins)
    except:
        exit(1)

    if flag == THE_FLAG:
        exit(0)
    exit(1)


if __name__ == "__main__":
    main()
