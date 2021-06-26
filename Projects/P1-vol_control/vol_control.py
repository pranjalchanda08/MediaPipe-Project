import sys
import cv2
import time
import math
import alsaaudio
import numpy as np

sys.path.append("../../")
import utils.hand_tracking as ht


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    cap.set(3, 1280)
    cap.set(4, 740)
    previous_time = 0
    track = ht.HandTracking()
    audio = alsaaudio.Mixer()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # # Read the frame
        success, img = cap.read()
        # # Flip input image horizontally
        flip_image = cv2.flip(img, 1)

        # Track and revert the image
        track.find_hand(flip_image)
        # Get all Landmarks
        pos_list_dict = track.find_all_landmarks(
            flip_image,
            hand_id_list=[0, 1],
            finger_list=None
        )
        # Process the landmark
        if len(pos_list_dict['0']) !=0:
            (x1,y1) , (x2,y2) = (pos_list_dict['0'][track.LM_DICT['THUMB_TIP']]), \
                                (pos_list_dict['0'][track.LM_DICT['INDEX_TIP']])

            cv2.circle(flip_image, (x1, y1), 15, (255,0,0), cv2.FILLED)
            cv2.circle(flip_image, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
            cv2.line(flip_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            length = int(math.hypot(x1-x2 , y1-y2))
            print((x1, y1), (x2, y2), length)
            if length < 30:
                mapped = 0
            elif length > 220:
                mapped = 100
            else:
                mapped = int(translate(length, left_min=30, left_max=220, right_min=0, right_max=100))
            if 0 <= mapped <= 100:
                audio.setvolume(mapped)

        # Calculate FPS
        if show_fps:
            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time
            # Include FPS text in image
            cv2.putText(flip_image,
                        "FPS: {}".format(int(fps)),
                        (10, 70),  # Position
                        cv2.FONT_HERSHEY_PLAIN,
                        1,  # Font size
                        (0, 0, 255),
                        2  # Thickness
                        )
        # Show the resultant image
        cv2.imshow("Output", flip_image)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(show_fps=True)