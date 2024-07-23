import requests
import nacl.utils
import nacl
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
from nacl.public import PrivateKey, Box, PublicKey
import nacl.secret
from nacl.secret import SecretBox
import os


def main():
    API_TOKEN = "6381a7b7b2775bce0eed150b1cd1668bbdc52e8a67518cb96434aa60a7b84764"
    GET_KEY_URL = "https://hash-browns.cs.uwaterloo.ca/api/surveil/get-key"
    SET_KEY_URL = "https://hash-browns.cs.uwaterloo.ca/api/surveil/set-key"
    SEND_URL = "https://hash-browns.cs.uwaterloo.ca/api/surveil/send"
    INBOX_URL = "https://hash-browns.cs.uwaterloo.ca/api/surveil/inbox"
    GOV_KEY = "dY2HwO5fuLe8UAtXHKuLeoIGYN3ZOtWirXDtw6QC0Xw="


    # PART 1

    sk = PrivateKey.generate()
    pk = sk.public_key
    
    body = {"api_token": API_TOKEN, "pubkey": str(pk.encode(encoder=Base64Encoder), 'utf-8')}

    r = requests.post(SET_KEY_URL, json=body)
    if r.status_code != 200:
        print(r.text)

    body = {"api_token": API_TOKEN, "user": "Muffin"}
    r = requests.post(GET_KEY_URL, json=body)
    if r.status_code != 200:
        print(r.text)
    
    muffin_pub_key = PublicKey((r.json())["pubkey"], Base64Encoder)

    gov_public_key = PublicKey(GOV_KEY, Base64Encoder)

    message_key = nacl.utils.random(SecretBox.KEY_SIZE)

    muffin_message_key = Box(sk, muffin_pub_key).encrypt(message_key)
    gov_message_key = Box(sk, gov_public_key).encrypt(message_key)

    message = SecretBox(message_key).encrypt(b"Muffin, I still need an answer! How long can you possibly take!!!")

    body = {"api_token": API_TOKEN, "recipient": "Muffin", "msg": str(Base64Encoder.encode(message), 'utf-8'),
            "recipient_key": str(Base64Encoder.encode(muffin_message_key), 'utf-8'), "gov_key": str(Base64Encoder.encode(gov_message_key), 'utf-8')}
    r = requests.post(SEND_URL, json=body)
    if r.status_code != 200:
        print(r.text)


    # PART 2

    





if __name__ == "__main__":
    main()