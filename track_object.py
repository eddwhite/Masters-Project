# Track Object
# **************
# The track controls all of the vehicles on a display
#
# Author: Edward White

import itertools
from vehicle_object import VehicleClass


class TrackClass:
    def __init__(self, vehicle_count):
        self.v = []
        # TODO: randomise vehicle positions
        for _ in itertools.repeat(None, vehicle_count):
            self.v.append(VehicleClass(0, 0))

    def get_vehicle_positions(self):
        res = []
        for v in self.v:
            res.append([v.x, v.y])
        return res

    def perform_routes(self, routes):
        result = []
        for i in range(len(routes)):
            actions = self.v[i].perform_route(routes[i])
            for a in actions:
                index = 0
                while index < len(result) and result[index].t < a.t:
                    index += 1
                result.insert(index, a)
        return result
