from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Mock license database
license_db = {"ABC123-XYZ789": "active"}

# Encryption key (For simplicity, using hardcoded key)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/validate', methods=['POST'])
def validate_license():
    data = request.get_json()
    license_key = data['license_key']
    encrypted_license = cipher_suite.encrypt(license_key.encode()).decode()

    if encrypted_license in license_db and license_db[encrypted_license] == "active":
        return jsonify({'status': 'valid'}), 200
    return jsonify({'status': 'invalid'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
