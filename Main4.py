import os
import time

from Main1 import load_license

def is_license_valid_offline():
    license_key = load_license()
    last_checked = os.path.getmtime('license.txt')  # Check the last modified time
    if time.time() - last_checked < 7 * 24 * 60 * 60:  # 7 days grace period
        return True
    return False

# Usage
if not is_license_valid_offline():
    print("Offline license validation failed.")
