class VehiclePIDController:
    """
    This class implements a PID controller for vehicle speed control.

    The VehiclePIDController is designed to maintain the desired speed of a
    vehicle by adjusting control outputs based on proportional, integral, and
    derivative terms, allowing for smoother and more efficient driving.
    """
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt

        self.integral = 0
        self.prev_error = 0

    def control(self, target_speed, current_speed):
        """
        Calculates the control output using a PID controller given the target and current speeds.

        Summary:
        This method computes the control signal based on the proportional, integral,
        and derivative terms derived from the target speed and current speed. The
        control signal is clamped between 0 and 1. This method updates the integral
        and derivative terms for the PID controller.

        Args:
            target_speed (float): The desired target speed.
            current_speed (float): The current speed.

        Returns:
            float: The control output, clamped between 0.0 and 1.0.

        """
        error = target_speed - current_speed
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error

        # Clamp output between 0 and 1
        output = max(0.0, min(output, 1.0))
        return output