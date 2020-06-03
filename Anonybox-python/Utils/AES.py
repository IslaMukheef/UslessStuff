from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode , b64encode
import hashlib

def setKey(myKey):
    hashed_key = hashlib.sha1(myKey.encode('UTF-8')).hexdigest()[:16]
    return(hashed_key)

def encrypt(stingtoencrypt,secret):
    try:
        #iv = get_random_bytes(AES.block_size) # we dont use iv, but you see it cuz isla wants to
        key = setKey(secret)
        cipher = AES.new(key.encode(), AES.MODE_CBC,  b'DaddayStalin4200')
        data = cipher.encrypt(pad(stingtoencrypt.encode(), 16))
        return b64encode(data)

    except:
        print('Error while encrypting')
        return 404

def decrypt(stingtodecrypt,secret):
    try:
        #iv = get_random_bytes(AES.block_size)# we dont use iv, but you see it cuz isla wants to
        key = setKey(secret)
        b64 =b64decode(stingtodecrypt)
        cipher = AES.new(key.encode(), AES.MODE_CBC,  b'DaddayStalin4200')
        data = unpad(cipher.decrypt(b64), 16)
        return data.decode()

    except:
        print('Error while decrypting')
        return 404
