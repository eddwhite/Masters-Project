# Flip Disc Display
# **************
# This is the display technology atop the generalised vehicle track.
# The flip disc display has bi-stable pixels, so the output is binary. When actuating, all pixels above the vehicle
# are actuated, even if they should be in the correct state. This reduces the chance of stuck pixels
#
# Author: Edward White

import numpy as np
from track_object import TrackClass


class FlipDiscDisplay:
    def __init__(self, track_width, track_height, pixel_subgrid_size, vehicle_count):
        self.pixels = 255 * np.ones((track_width * pixel_subgrid_size, track_height * pixel_subgrid_size, 3), np.uint8)
        self.t_width = track_width
        self.t_height = track_height
        self.pix_size = pixel_subgrid_size
        self.track = TrackClass(vehicle_count)
        self.actions = []

    # def route_outcome(self):
    #     for a in self.actions:
    #         for row in range(self.pix_size):
    #             for col in range(self.pix_size):
    #                 self.pixels[self.t_height * self.pix_size + row][self.t_width * self.pix_size + col] = \
    #                 a.pixels[row][col]

    def perform_route(self, routes):
        self.actions = self.track.perform_routes(routes)

    def get_route_time(self):
        return self.actions[-1].t

    def realtime_animation(self, t):
        for a in self.actions:
            if a.t <= t:
                for row in range(self.pix_size):
                    for col in range(self.pix_size):
                        self.pixels[a.x * self.pix_size + row][a.y * self.pix_size + col] = a.pixels[col][row]
        return self.pixels

