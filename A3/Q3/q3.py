import requests
import nacl.utils
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
import os

def main():
    API_TOKEN = "6381a7b7b2775bce0eed150b1cd1668bbdc52e8a67518cb96434aa60a7b84764"
    SET_KEY_URL = "https://hash-browns.cs.uwaterloo.ca/api/signed/set-key"
    SENG_MSG_URL = "https://hash-browns.cs.uwaterloo.ca/api/signed/send"

    # PART 1

    # To preserve the signing key for Part 2
    if not os.path.exists("signing_key"):
        signing_key = SigningKey.generate()
        with open("signing_key", "wb") as signing_key_file:
            # encode the signed key using Base64 then write the raw bytes to file
            signing_key_file.write(signing_key.encode(encoder=Base64Encoder))
    else:
        with open("signing_key", "rb") as signing_key_file:
            # Read the raw bytes from file and decode using Base64, then regenerate the signing key
            signing_key = SigningKey(bytes(signing_key_file.read()), encoder=Base64Encoder)
            print(signing_key.encode(Base64Encoder))
            

    verify_key = signing_key.verify_key.encode(encoder=Base64Encoder)

    body = {"api_token": API_TOKEN, "pubkey": str(verify_key, 'utf-8')}

    r = requests.post(SET_KEY_URL, json=body)
    if r.status_code != 200:
        print(r.text)

    # PART 2

    message = signing_key.sign(b"Muffin, attack on ECorp is scheduled for 8:00 hours.", encoder=Base64Encoder)

    body = {"api_token": API_TOKEN, "recipient": "Muffin", "msg": str(message, 'utf-8')}

    r = requests.post(SENG_MSG_URL, json=body)
    if r.status_code != 200:
        print(r.text)




if __name__ == "__main__":
    main()