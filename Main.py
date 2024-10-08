import requests
import json
import os
import time
import logging

# ---- Logging Setup ----
logging.basicConfig(filename='license_activity.log', level=logging.INFO)

# ---- License Storage Functions ----
def store_license_locally(license_key, status="active", last_validated=None, expiration=None):
    """Stores license data in the local license.txt file."""
    last_validated = last_validated or time.time()  # Use current time if not provided
    expiration = expiration or (time.time() + 30 * 24 * 60 * 60)  # Default 30 days expiration
    
    with open('license.txt', 'w') as file:
        file.write(f"License Key: {license_key}\n")
        file.write(f"Status: {status}\n")
        file.write(f"Last Validated: {int(last_validated)}\n")
        file.write(f"Expiration: {int(expiration)}\n")

def load_license():
    """Loads license data from the local license.txt file."""
    if not os.path.exists('license.txt'):
        return None
    
    license_info = {}
    with open('license.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(": ")
            license_info[key] = value
    
    return license_info

# ---- Online License Validation ----
def online_validate_license(license_key):
    """Attempts to validate the license online by communicating with the central server."""
    try:
        server_url = "https://license-server.com/validate"  # Example server URL
        headers = {'Content-Type': 'application/json'}
        data = {'license_key': license_key}
        
        response = requests.post(server_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'invalid', 'message': 'Validation failed'}
    except Exception as e:
        raise Exception(f"Error connecting to the license server: {e}")

# ---- Offline License Validation ----
def is_license_valid_offline():
    """Checks if the license is still valid based on the locally stored data."""
    license_data = load_license()
    if not license_data:
        return False
    
    current_time = time.time()

    # Check if license is active
    if license_data['Status'] != 'active':
        return False

    # Check if license has expired
    if current_time > int(license_data['Expiration']):
        return False

    # Check grace period (e.g., 7 days since last validation)
    last_validated = int(license_data['Last Validated'])
    grace_period = 7 * 24 * 60 * 60  # 7 days in seconds
    if current_time - last_validated > grace_period:
        return False

    return True

# ---- License Validation Workflow ----
def validate_license(license_key):
    """Main validation flow that tries online validation first, then offline fallback."""
    try:
        # Try to validate the license online
        result = online_validate_license(license_key)
        if result['status'] == 'valid':
            print("License validated online.")
            # Store the license info locally for future offline use
            result['last_validated'] = time.time()
            store_license_locally(license_key, result['status'], result['last_validated'], result.get('expiration'))
            log_license_activity('License validated online and saved locally.')
            return True
        else:
            print("License validation failed online.")
            return False
    except Exception as e:
        # If online validation fails, fallback to offline validation
        print(f"Online validation failed: {e}")
        if is_license_valid_offline():
            print("Offline validation passed.")
            log_license_activity('License validated offline.')
            return True
        else:
            print("Offline validation failed.")
            log_license_activity('License validation failed offline.')
            return False

# ---- Re-validation When Back Online ----
def update_license_when_online(license_key):
    """Re-validates and updates license when the client reconnects to the internet."""
    try:
        result = online_validate_license(license_key)
        if result['status'] == 'valid':
            print("License re-validated online, updating local data.")
            result['last_validated'] = time.time()
            store_license_locally(license_key, result['status'], result['last_validated'], result.get('expiration'))
            log_license_activity('License re-validated and updated online.')
        else:
            print("License is no longer valid.")
    except Exception as e:
        print(f"Could not validate license online: {e}")

# ---- License Activity Logging ----
def log_license_activity(activity):
    """Logs license activities like validation and updates."""
    logging.info(f"{activity} - Time: {time.ctime()}")

# ---- Usage Example ----
if __name__ == "__main__":
    # Example license key (In real scenarios, this would be dynamically provided)
    license_key = "ABC123-XYZ789"

    # Validate the license using the online and offline fallback approach
    if validate_license(license_key):
        print("License is valid.")
    else:
        print("License is invalid.")

    # Re-validate and update the license when online connection is restored
    # This can be scheduled to run periodically, e.g., every time the app is launched
    update_license_when_online(license_key)
