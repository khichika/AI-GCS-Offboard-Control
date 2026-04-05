import cv2
from ultralytics import YOLO
import sys
import os

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.drone_params import CONFIG
from tracker import PIDController
from crsf_tx import CRSFDriver

class AIGroundStation:
    def __init__(self):
        print("[*] Initializing AI-GCS...")
        self.model = YOLO("yolov8n.pt") # Light model for fast speed
        self.cap = cv2.VideoCapture(CONFIG["camera_index"])
        
        self.crsf = CRSFDriver(CONFIG["serial_port"], CONFIG["baud_rate"])
        
        self.pid_yaw = PIDController(**CONFIG["pid_yaw"])
        self.pid_pitch = PIDController(**CONFIG["pid_pitch"])

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret: break

            height, width, _ = frame.shape
            center_x, center_y = width // 2, height // 2

            # YOLO working
            results = self.model(frame, stream=True, verbose=False)
            
            target_found = False
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    if cls == 0:  # 0 = person (human)
                        target_found = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        obj_x = (x1 + x2) // 2
                        obj_y = (y1 + y2) // 2

                        # Visualisation
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (obj_x, obj_y), 5, (0, 0, 255), -1)

                        # Calculate mistake and PID
                        error_x = obj_x - center_x
                        error_y = obj_y - center_y

                        yaw_adj = self.pid_yaw.update(error_x)
                        pitch_adj = self.pid_pitch.update(error_y)

                        # Send via CRSF
                        rc_yaw = CONFIG["rc_mid"] + yaw_adj
                        rc_pitch = CONFIG["rc_mid"] - pitch_adj # Y-axis inversion
                        
                        self.crsf.send_rc(roll=1500, pitch=rc_pitch, throttle=1000, yaw=rc_yaw)
                        break # Tracking the first target only

            if not target_found:
                # If the target lost - stay in the center
                self.crsf.send_rc(1500, 1500, 1000, 1500)

            # Aim in the center of the frame
            cv2.circle(frame, (center_x, center_y), 3, (255, 0, 0), -1)
            cv2.imshow("AI-GCS Feedback", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.display.destroyAllWindows()

if __name__ == "__main__":
    gcs = AIGroundStation()
    gcs.run()
