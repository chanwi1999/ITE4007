from Crypto import Random
from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
import hashlib
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def printInfo(enc, dec):
    print('encrypted: ')
    print(enc)
    print('decrypted: ')
    print(dec.decode())

def padding(msg, length):
    while len(msg)%length != 0:
        msg += ' '
    return msg.encode('utf-8')

def aes(msg):
    key = input('key(16/24/32): ')
    if (len(key) != 16 and len(key) != 24 and len(key) != 32):
        print('[warning] temporary key is "1234567812345678"')
        key = '1234567812345678'
    key = key.encode('utf-8')
    iv = Random.new().read(AES.block_size)

    aes_e = AES.new(key, AES.MODE_CBC, iv)
    enc = aes_e.encrypt(msg)

    aes_d = AES.new(key, AES.MODE_CBC, iv)
    dec = aes_d.decrypt(enc)

    printInfo(enc, dec)

def des(msg):
    key = input('key(8): ')
    if (len(key) != 8):
        print('[warning] temporary key is "12345678"')
        key = '12345678'
    key = key.encode('utf-8')

    des_e = DES.new(key, DES.MODE_ECB)    
    enc = des_e.encrypt(msg)

    des_d = DES.new(key, DES.MODE_ECB)
    dec = des_d.decrypt(enc)

    printInfo(enc, dec)

def arc4(msg):
    key = input('key: ')
    if (len(key) == 0):
        print('[warning] temporary key is "1234"')
        key = '1234'
    key = key.encode('utf-8')

    arc4_e = ARC4.new(key)
    enc = arc4_e.encrypt(msg)

    arc4_d = ARC4.new(key)
    dec = arc4_d.decrypt(enc)

    printInfo(enc, dec)

def rsa(msg):
    num = input('key length(>= 1024): ')
    if (len(num) == 0 or num.isdigit() == False or int(num) < 1024):
        print('[warning] temporary key length is 1024')
        num = 1024
    PR = RSA.generate(int(num))
    PU = PR.publickey()

    enct = PKCS1_OAEP.new(PU)
    enc = enct.encrypt(msg)

    dect = PKCS1_OAEP.new(PR)
    dec = dect.decrypt(enc)

    printInfo(enc, dec)

def main():

    msg = input('original message: ')
    while msg == '':
        msg = input('original message: ')
    
    act = input('\ncipher type(DES/AES/ARC4): ')
    if (act == 'DES'):
        des(padding(msg, DES.block_size))
    elif (act == 'AES'):
        aes(padding(msg, AES.block_size))
    elif (act == 'ARC4'):
        arc4(padding(msg, ARC4.block_size))
    else:
        print('[warning] temporary DES executed')
        des(padding(msg, DES.block_size))

    act = input('\nhash type(SHA/SHA256/SHA384/SHA512): ')
    if (act == 'SHA'):
        res = hashlib.sha1(msg.encode('utf-8'))
    elif (act == 'SHA256'):
        res = hashlib.sha256(msg.encode('utf-8'))
    elif (act == 'SHA384'):
        res = hashlib.sha384(msg.encode('utf-8'))
    elif (act == 'SHA512'):
        res = hashlib.sha512(msg.encode('utf-8'))
    else:
        print('[warning] temporary SHA executed')
        res = hashlib.sha1(msg.encode('utf-8'))
    print(res.hexdigest())

    print('\nRSA')
    rsa(msg.encode('utf-8'))

main()
