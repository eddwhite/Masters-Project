# This takes an input video, converts it to B&W and scales it to the correct size

import cv2
import subprocess as sp
import numpy as np
import os


def main():
    input_video = 'far_away.mp4'
    output_video = 'far_away_b&w.avi'

    # OpenCV video input
    v_in = cv2.VideoCapture(input_video)

    # Get input video details
    v_width = int(v_in.get(cv2.CAP_PROP_FRAME_WIDTH))
    v_height = int(v_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
    v_fps = v_in.get(cv2.CAP_PROP_FPS)

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

    while v_in.isOpened():
        ret, frame = v_in.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to greyscale
            frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # b&w
            frame = cv2.resize(frame, (v_width, v_height), interpolation=cv2.INTER_CUBIC)  # resize
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

            # Convert numpy array to character stream
            if frame.dtype != np.uint8:
                frame = frame.astype('uint8')
            pipe.stdin.write(frame.tostring())
        else:
            break

    v_in.release()
    cv2.destroyAllWindows()
    pipe.stdin.close()
    pipe.wait()


if __name__ == "__main__":
    main()
