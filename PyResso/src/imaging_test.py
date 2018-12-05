import numpy as np
import cv2
from Communication.capture import FrameSource

import imutils

def main():
    cap = cv2.VideoCapture(0)
    # cap.start()
    while True:

        ret, frame = cap.read()
        # cv2.imshow("TEST", frame)
        frame2 = imutils.convenience.is_cv3()


        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    


if __name__ == "__main__":
    main()