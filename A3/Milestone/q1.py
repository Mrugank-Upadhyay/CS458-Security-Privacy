import requests
import base64


# CONST URLs 
SEND_URL = "https://hash-browns.cs.uwaterloo.ca/api/plain/send"
INBOX_URL = "https://hash-browns.cs.uwaterloo.ca/api/plain/inbox"


def main():
    api_token = "6381a7b7b2775bce0eed150b1cd1668bbdc52e8a67518cb96434aa60a7b84764"


    # PART 1 - Sending a message to Muffin
    
    message = base64.b64encode(b"Hey there Muffin, hopefully Eve doesn't see this message!").decode('utf-8')
    body = {"api_token": api_token, "recipient": "Muffin", "msg": message}

    r = requests.post(SEND_URL, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, json=body)
    if r.status_code != 200:
        print(r.text)

    
    # PART 2 - Receiving a message from Muffin

    body = {"api_token": api_token}
    
    r = requests.post(INBOX_URL, headers={"Content-Type": "application/json", "Accept": "application/json"}, json=body)

    message = base64.b64decode(r.json()[0]["msg"]).decode('utf8')
    print(f"Message from Muffin is '{message}'")

if __name__ == "__main__":
    main()
