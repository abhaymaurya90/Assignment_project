import requests
import json
import os

def validate_license(license_key):
    server_url = "https://license-server.com/validate"
    headers = {'Content-Type': 'application/json'}
    data = {'license_key': license_key}
    response = requests.post(server_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Validation failed'}

def store_license(license_key):
    with open('license.txt', 'w') as f:
        f.write(license_key)

def load_license():
    if os.path.exists('license.txt'):
        with open('license.txt', 'r') as f:
            return f.read()
    return None

# Usage
license_key = load_license()
if not license_key:
    license_key = "ABC123-XYZ789"
    store_license(license_key)

result = validate_license(license_key)
print(result)
