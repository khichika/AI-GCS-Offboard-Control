# Hardware and leading configuration
CONFIG = {
    "camera_index": 0,          # Skydroid index (0, 1 or 2)
    "serial_port": "COM3",      # HappyModel ELRS module port (Windows COM, Linux /dev/ttyUSB0)
    "baud_rate": 420000,        # Default CRSF speed

    # Leading (1000 - 2000 us)
    "rc_mid": 1500,
    "rc_min": 1000,
    "rc_max": 2000,
    
    # PIDs for Yaw & Pitch (drone/camera tilt)
    "pid_yaw": {"P": 0.5, "I": 0.01, "D": 0.1},
    "pid_pitch": {"P": 0.4, "I": 0.01, "D": 0.1}
}
