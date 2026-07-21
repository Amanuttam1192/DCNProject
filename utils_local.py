import time
import cv2
from config import SNAPSHOT_PATH, SAVE_SNAPSHOT_ON_ALERT

def cooldown_passed(last_alert_time, cooldown):
    """Check if cooldown period has passed."""
    return (time.time() - last_alert_time) >= cooldown

def save_snapshot(frame):
    """Save snapshot image if enabled."""
    if SAVE_SNAPSHOT_ON_ALERT:
        cv2.imwrite(SNAPSHOT_PATH, frame)
        print(f"📸 Snapshot saved to {SNAPSHOT_PATH}")
