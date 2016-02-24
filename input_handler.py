# This takes an input video, converts it to B&W and scales it to the correct size

import cv2
import numpy as np

def main():
    input_video = 'test.avi'
    output_video = 'output.avi'
    output_size = (width, height)

    v_in = cv2.VideoCapture(input_video)
    v_out = cv2.VideoWriter(output_video, -1, v_in.get('CV_CAP_PROP_FPS'), output_size)

    while v_in.isOpened():
        ret, f_in = v_in.read()

        f_in = cv2.cvtColor(f_in, cv2.COLOR_BGR2GRAY)  # convert to greyscale
        f_in = cv2.adaptiveThreshold(f_in, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # b&w

        f_out = cv2.resize(f_in, output_size, interpolation=cv2.INTER_CUBIC)
        v_out.write(f_out)

    v_out.release()
    v_in.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()