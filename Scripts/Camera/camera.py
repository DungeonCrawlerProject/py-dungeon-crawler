import math
from typing import Tuple


class Camera:

    def __init__(self):

        # It is assumed that this will probably be needed for the movement logic
        self.damping: float = 0.5
        self.offset: Tuple[float, float] = (0.0, 0.0)
        self.velocity: Tuple[float, float] = (0, 0)

    def update(self):
        # Needs completely different concept for implementation
        raise NotImplementedError

    # This is included below for potential use for dampening the camera.
    @staticmethod
    def smooth_damp(current_position, target_position, current_velocity, damping_ratio, delta_time=0.1):
        # Calculate the angular frequency
        omega_n = math.sqrt(1.0 - damping_ratio ** 2)

        # Calculate the exponential decay factor
        exp_term = math.exp(-damping_ratio * omega_n * delta_time)

        # Calculate the under damped response
        c = 1.0 / omega_n
        underdamped_response = c * exp_term * math.sin(
            omega_n * delta_time + math.atan(damping_ratio / math.sqrt(1.0 - damping_ratio ** 2)))

        # Update the position and velocity
        new_position = target_position + (
                    current_position - target_position + c * current_velocity) * exp_term * math.cos(
            omega_n * delta_time) + underdamped_response
        new_velocity = -omega_n * exp_term * (
                    current_position - target_position) + exp_term * current_velocity + underdamped_response

        return new_position, new_velocity


