import requests
import nacl.secret
import nacl.utils
from nacl.encoding import Base64Encoder



def main():

    PSK_SEND = "https://hash-browns.cs.uwaterloo.ca/api/psk/send"
    PSK_INBOX = "https://hash-browns.cs.uwaterloo.ca/api/psk/inbox"
    API_TOKEN = "6381a7b7b2775bce0eed150b1cd1668bbdc52e8a67518cb96434aa60a7b84764"
    PRE_SHARED_KEY = "cc14776c3261b8ad094ddadcf4724b31966a4e8b497560be7698ad9c1c1739bb"
    
    # PART 1
    DECODED_KEY = bytes.fromhex(PRE_SHARED_KEY)
    BOX = nacl.secret.SecretBox(DECODED_KEY)

    message = b"Hey Muffin, thanks for giving me your secret key magically!"
    cipher_text = str(Base64Encoder.encode(BOX.encrypt(message)), 'utf-8')

    body = {"api_token": API_TOKEN, "recipient": "Muffin", "msg": cipher_text}

    r = requests.post(PSK_SEND, json=body)
    if r.status_code != 200:
        print(r.text)
    

    # PART 2
    r = requests.post(PSK_INBOX, json={"api_token": API_TOKEN})
    print(f"Message from Muffin is '{BOX.decrypt(Base64Encoder.decode(r.json()[0]['msg'])).decode('utf-8')}'")


if __name__ == "__main__":
    main()
