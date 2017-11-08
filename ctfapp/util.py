import json
from hashlib import md5
from random import randint
from time import time
from wtforms import ValidationError
from binascii import hexlify, unhexlify
from ecdsa import SigningKey, VerifyingKey, NIST384p


def build_coin(username, sk_pem, amount):
    coin = {}
    sk = SigningKey.from_pem(sk_pem)
    coin['MN'] = 'F9BEB4E1'
    coin['NC'] = str(randint(0, 999999)).zfill(6)
    coin['AM'] = str(amount)
    coin['TS'] = str(int(time()))
    coin['OW'] = username
    coin['CU'] = 'NIST384'
    coin['PK'] = hexlify(sk.get_verifying_key().to_string()).decode('utf-8')
    # sign all this
    text = json.dumps(coin, sort_keys=True).encode('utf-8')
    coin['SIG'] = hexlify(sk.sign(text)).decode('utf-8')
    return json.dumps(coin, sort_keys=True)


def check_coin(data, username, sk_pem):
    c = {}
    sk = SigningKey.from_pem(sk_pem)

    # build coin from json
    try:
        c['MN'] = data['MN']
        c['NC'] = data['NC']
        c['AM'] = data['AM']
        c['TS'] = data['TS']
        c['OW'] = data['OW']
        c['CU'] = data['CU']
        c['PK'] = data['PK']
    except:
        raise ValidationError( "Could not parse json!")

    if not isinstance(c['AM'], str):
        raise ValidationError('AM must be a string!')
    if not isinstance(c['NC'], str):
        raise ValidationError('NC must be a string!')
    if not isinstance(c['TS'], str):
        raise ValidationError('TS must be a string!')

    # check the fields for valid data
    if c['MN'] != 'F9BEB4E1':
        raise ValidationError('Wrong magic number!')
    if len(c['NC']) != 6 or not c['NC'].isdigit():
        raise ValidationError('Nonce Malformed!')
    if not c['AM'].isdigit():
        raise ValidationError('Amount must be a number!')
    if len(c['TS']) != 10 or not c['TS'].isdigit():
        raise ValidationError('Nonce Malformed!')
    if c['OW'] != username:
        raise ValidationError('You do not own this coin!')
    if c['CU'] != 'NIST384':
        raise ValidationError('Wrong curve!')

    # get the pk
    try:
        PK_string = unhexlify(c['PK'])
        PK = VerifyingKey.from_string(PK_string, curve=NIST384p)
    except:
        raise ValidationError('The public key is damaged!')

    # check if the correct PK is used
    if sk.get_verifying_key().to_string() != PK_string:
        raise ValidationError('Public key changed!')

    # check the signature
    try:
        sig = unhexlify(data['SIG'])
        text = json.dumps(c, sort_keys=True).encode('utf-8')
        PK.verify(sig, text)
    except:
        raise ValidationError('Wrong signature!')


def get_coin_MD5(data):
    c = {}
    # build coin from json
    try:
        c['MN'] = data['MN']
        c['NC'] = data['NC']
        c['AM'] = data['AM']
        c['TS'] = data['TS']
        c['OW'] = data['OW']
        c['CU'] = data['CU']
        c['PK'] = data['PK']
        # this was bugged
        c['SIG'] = data['SIG'].lower()
    except:
        raise ValidationError('Could not parse json for MD5!')

    try:
        j = json.dumps(c, sort_keys=True)
        h = md5(j.encode('utf-8')).hexdigest()
    except:
        raise ValidationError('Something went wrong!')

    return h
