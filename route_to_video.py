import collections
import numpy as np
import cv2
from flip_disc_display import FlipDiscDisplay
import math


def main():
    # Initialise a display
    display = FlipDiscDisplay(4, 3, 5, 1)

    # Create a route
    step = collections.namedtuple('step', ['cmd', 'value'])
    v1 = []
    for col in range(0, 3):
        v1.append(step('east', 1))
        v1.append(step('actuate', 0 * np.ones((5, 5, 3), np.uint8)))

    r = [v1]

    # Perform route and get length
    display.perform_route(r)
    video_length = math.ceil(display.get_route_time()) + 1

    fps = 15
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIB ')
    out = cv2.VideoWriter('output.avi', -1, fps, (3*5, 4*5), 1)

    for t in np.linspace(0, video_length, num = video_length * fps):
        frame = display.realtime_animation(t)
        out.write(frame)
        cv2.imshow('Simulation', frame)
        if cv2.waitKey(1000 / fps) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
