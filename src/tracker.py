import time

class PIDController:
    def __init__(self, p, i, d, limit=500):
        self.kp = p
        self.ki = i
        self.kd = d
        self.limit = limit # max deviation from 1500
        
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.time()

    def update(self, error):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0.0: dt = 0.01

        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.prev_error = error
        self.last_time = current_time

        # Limit output (ex., max +/- 500 from center)
        return max(-self.limit, min(self.limit, output))
