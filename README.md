# Autonomous Ground Control Station (AI-GCS) 🚁🛰

## Overview
This project implements a fully autonomous control loop for a standard FPV UAV (Mark4 / SP Racing F3) using a PC-based Ground Control Station. The system replaces the human pilot by processing video telemetry and generating RC control signals via an external ELRS transmitter.

## Hardware Stack
* **UAV:** Mark4 7" frame, SP Racing F3 FC, ELRS 2.4G RX.
* **Video Link:** 5.8G VTX -> Skydroid 5.8G Receiver (USB to PC).
* **Control Link:** PC -> HappyModel ES24TX Pro (1000mW) -> ELRS 2.4G.
* **Processing:** PC (Python + YOLO) as the primary Decision Making Unit.

## System Workflow
1.  **Vision:** PC receives 5.8G video via Skydroid. OpenCV captures the stream.
2.  **AI Inference:** YOLO neural network detects the target and calculates the offset from the frame center.
3.  **Link Integration:** The Python script calculates RC channel values (1000-2000µs) and transmits them to the **HappyModel ES24TX Pro** module via Serial (CRSF protocol).
4.  **Execution:** The drone receives standard ELRS signals and reacts as if commanded by a high-precision pilot.

## Key Technical Features
* **Low-Latency AI:** Optimized YOLO inference for real-time tracking.
* **Direct CRSF Implementation:** Custom Python driver for HappyModel ELRS modules to bypass standard flight GCS software.
* **Non-Invasive Autonomy:** Works with any "dumb" FPV drone without modifying onboard firmware.

## How to use
1. Connect Skydroid 5.8G and HappyModel ES24TX Pro to USB ports.
2. Configure serial ports in `config/drone_params.py`.
3. Run `python src/main.py`.
