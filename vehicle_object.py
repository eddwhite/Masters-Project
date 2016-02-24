# Vehicle Object
# **************
# The vehicle returns a list of the pixels changed and the time it occurs.
# TODO: expand it to give a list of positions it is in (including when it occupies both) for collision detection
#
# Author: Edward White

import math
import collections


class VehicleClass:

    # Dummy values being used for now. Use SI units
    actuate_time = 2
    accel = 1
    grid_dist = 10
    deccel = 1
    max_speed = 1

    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start

    # Simple linear approximation of movement characteristics
    def get_move_time(self, distance):
        d = distance * self.grid_dist
        minmax_dist_speed = 0.5 * ((self.max_speed ** 2 / self.accel) + (self.max_speed ** 2 / self.deccel))
        if distance > minmax_dist_speed:
            return self.max_speed / self.accel + self.max_speed / self.deccel + (d - minmax_dist_speed) / self.max_speed
        else:
            return math.sqrt(2 * d * ((self.accel + self.deccel) / (self.accel * self.deccel)))

    def perform_route(self, path):
        result = []
        t = 0
        actuate = collections.namedtuple('actuate', ['t', 'x', 'y', 'pixels'])
        for p in path:
            if p.cmd == 'wait':
                t += p.value
            elif p.cmd == 'actuate':
                t += self.actuate_time
                result.append(actuate(t, self.x, self.y, p.value))
            else:
                if p.cmd == 'north':
                    self.y -= p.value
                elif p.cmd == 'south':
                    self.y += p.value
                elif p.cmd == 'west':
                    self.x -= p.value
                else:  # east
                    self.x += p.value
                t += self.get_move_time(p.value)
        return result
