import time
import cv2
from detector import load_model, get_elephant_class_id, detect_elephant
from alert import send_sms_twilio
from utils_local import cooldown_passed, save_snapshot
from config import WEBCAM_INDEX, CONFIDENCE_THRESHOLD, COOLDOWN_SECONDS

def main():
    model = load_model()
    elephant_id = get_elephant_class_id(model)
    print(f"Using class ID {elephant_id} for 'elephant'.")

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print("Cannot open webcam. Exiting.")
        return

    last_alert_time = 0
    print("Starting webcam. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame read failed. Retrying...")
            time.sleep(0.5)
            continue

        detected, frame = detect_elephant(frame, model, elephant_id)

        if detected and cooldown_passed(last_alert_time, COOLDOWN_SECONDS):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            text = f"ହାତୀ ଚିହ୍ନଟ ହେଲା Elephant detected at {timestamp} (Confidence ≥ {CONFIDENCE_THRESHOLD})."
            save_snapshot(frame)
            print("Sending SMS alert...")
            send_sms_twilio(text)
            last_alert_time = time.time()

        cv2.imshow('Elephant Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
