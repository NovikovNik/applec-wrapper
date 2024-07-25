import jwt
import time
import requests

KEY_ID = 'key_id'
ISSUER_ID = 'user_id'
EXPIRATION_TIME = 100000
PRIVATE_KEY_PATH = 'key_path.p8'

def load_private_key(path):
    with open(path, 'r') as f:
        return f.read()

def generate_apple_connect_token():
    current_time = int(time.time())
    
    headers = {
        'alg': 'ES256',
        'kid': KEY_ID,
        'typ': 'JWT'
    }
    
    payload = {
        "sub": "user",
        'iat': current_time,
        'exp': current_time + EXPIRATION_TIME,
        'aud': 'appstoreconnect-v1'
    }
    
    key_string = load_private_key(PRIVATE_KEY_PATH)
    print(key_string)
    token = jwt.encode(payload, key_string, algorithm='ES256', headers=headers)
    return token

def get_app_store_data(token):
    url = "https://api.appstoreconnect.apple.com/v1/apps"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

token = generate_apple_connect_token()
print(f"Generated JWT token: {token.decode()}")

app_data = get_app_store_data(token.decode())
print(app_data)