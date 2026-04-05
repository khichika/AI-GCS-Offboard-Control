# Autonomous Ground Control Station (AI-GCS)

![Hardware Setup]([LINK TO HARDWARE])

## 1. Executive Summary
This project implements a fully autonomous control loop for a standard FPV UAV (Mark4 / SP Racing F3) using a PC-based Ground Control Station. It shifts the heavy computational burden of Computer Vision (CV) from the airborne platform to the ground. The system replaces the human pilot by processing video telemetry and generating RF control signals via an external ELRS transmitter.

## 2. Hardware Stack
* **UAV:** Mark4 7" frame, SP Racing F3 FC, ELRS 2.4G RX.
* **Video Link:** 5.8G Analog VTX -> Skydroid 5.8G Receiver (USB to PC).
* **Control Link:** PC -> HappyModel ES24TX Pro (1000mW) -> ELRS 2.4G RX.
* **Decision Making Unit:** PC running Python & YOLOv8.

## 3. System Workflow
1. **Perception:** PC receives 5.8G video via Skydroid. OpenCV captures the stream.
2. **Inference:** YOLO neural network detects the target and calculates the offset from the frame center.
3. **Control Loop:** Custom PID controllers translate spatial errors into RC channel values (1000-2000µs).
4. **RF Uplink:** The Python script packs data into the **CRSF Protocol** and transmits it directly to the HappyModel ES24TX Pro module via Serial.

![Inference Demo]([LINK TO THE GIF-ANIMATION])

## 4. Key Technical Features
* **Direct CRSF Implementation:** Custom low-level Python driver for HappyModel ELRS modules to bypass standard flight GCS software.
* **Non-Invasive Autonomy:** Works with any standard "dumb" FPV drone without modifying onboard firmware.

## 5. Setup & Execution
```bash
pip install -r requirements.txt
# Update COM-port and camera index in config/drone_params.py
python src/main.py
