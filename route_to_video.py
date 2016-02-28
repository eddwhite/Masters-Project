import collections
import os
import numpy as np
import cv2
from flip_disc_display import FlipDiscDisplay
import math
import subprocess as sp


def main():
    # Initialise
    v_width = 3*5;
    v_height = 4*5;
    output_video = 'output_test.avi'
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

    v_fps = 15
    # FFMPEG Video output
    FFMPEG_BIN = 'C:/ffmpeg/bin/ffmpeg.exe'
    command = [FFMPEG_BIN,
               '-y',  # (optional) overwrite output file if it exists
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-s', '%dx%d'% (v_width, v_height),  # size of one frame
               '-pix_fmt', 'rgb24',
               '-r', '%.02f' % v_fps,  # frames per second
               '-i', '-',  # The imput comes from a pipe
               '-an',  # Tells FFMPEG not to expect any audio
               '-vcodec', 'png',
               output_video]
    pipe = sp.Popen(command, stdout=open(os.devnull, 'wb'), stdin=sp.PIPE, stderr=None)

    for t in np.linspace(0, video_length, num=video_length * v_fps):
        frame = display.realtime_animation(t)
        # Write frame to file
        if frame.dtype != np.uint8:
                frame = frame.astype('uint8')
        pipe.stdin.write(frame.tostring())

        # Display video
        cv2.imshow('Simulation', frame)
        if cv2.waitKey(1000 / v_fps) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    pipe.stdin.close()
    pipe.wait()


if __name__ == "__main__":
    main()
