import logging
import time

logging.basicConfig(filename='license_activity.log', level=logging.INFO)

def log_license_activity(activity):
    logging.info(f"{activity} - Time: {time.ctime()}")

# Usage
log_license_activity('License validated for key ABC123')
