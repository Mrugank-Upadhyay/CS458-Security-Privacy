import requests
import nacl.utils
import nacl
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
from nacl.public import PrivateKey, Box, PublicKey
from nacl.secret import SecretBox
from nacl.hash import blake2b
import os


def main():
    API_TOKEN = "6381a7b7b2775bce0eed150b1cd1668bbdc52e8a67518cb96434aa60a7b84764"
    GET_KEY_URL = "https://hash-browns.cs.uwaterloo.ca/api/pke/get-key"
    SET_KEY_URL = "https://hash-browns.cs.uwaterloo.ca/api/pke/set-key"
    SEND_URL = "https://hash-browns.cs.uwaterloo.ca/api/pke/send"
    INBOX_URL = "https://hash-browns.cs.uwaterloo.ca/api/pke/inbox"

    # PART 1

    body = {"api_token": API_TOKEN, "user": "Muffin"}

    r = requests.post(GET_KEY_URL, json=body)
    if r.status_code != 200:
        print(r.text)

    retJson = r.json()
    pub_key = retJson["pubkey"]

    retHash = blake2b(Base64Encoder.decode(pub_key))

    print(f"hash returned is {str(retHash, 'utf-8')}")


    # PART 2

    sk = PrivateKey.generate()
    pk = sk.public_key
    pub_key = PublicKey(pub_key, Base64Encoder)

    body = {"api_token": API_TOKEN, "pubkey": str(pk.encode(encoder=Base64Encoder), 'utf-8')}

    r = requests.post(SET_KEY_URL, json=body)
    if r.status_code != 200:
        print(r.text)


    message = b"Muffin, I need an answer... are you in?"
    box = Box(sk, pub_key)
    cipher_text = box.encrypt(message, encoder=Base64Encoder)

    body = {"api_token": API_TOKEN, "recipient": "Muffin", "msg": str(cipher_text, 'utf-8')}

    r = requests.post(SEND_URL, json=body)
    if r.status_code != 200:
        print(r.text)
    
    # PART 3

    r = requests.post(INBOX_URL, json={"api_token": API_TOKEN})
    if r.status_code != 200:
        print(r.text)

    encrypted_message = r.json()[0]["msg"]
    decrypted_message = box.decrypt(ciphertext=encrypted_message, encoder= Base64Encoder).decode('utf-8')
    print(f"Message from Muffin '{decrypted_message}'")



    

    

if __name__ == "__main__":
    main()

