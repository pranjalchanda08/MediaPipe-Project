try:
    import sys
    import cv2
    import time
    import math
    import numpy as np
    import utils.hand_tracking as ht
except ModuleNotFoundError:
    sys.path.append("../")
finally:
    import utils.hand_tracking as ht


def vector_len(a_tup, b_tup):
    return int(math.hypot(a_tup[0] - b_tup[0], a_tup[1] - b_tup[1]))


def angle(vector1_a, vector1_b, vector2_a, vector2_b):
    try:
        m1 = (vector1_a[1] - vector1_b[1]) / (vector1_a[0] - vector1_b[0])
        theta1 = math.atan(m1)

        m2 = (vector2_a[1] - vector2_b[1]) / (vector2_a[0] - vector2_b[0])
        theta2 = math.atan(m2)

        return math.degrees(theta1 - theta2)
    except ZeroDivisionError:
        return 0


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    cap.set(3, 1280)
    cap.set(4, 740)
    previous_time = 0
    track = ht.HandTracking()

    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # # Read the frame
        success, img = cap.read()
        # # Flip input image horizontally
        flip_image = cv2.flip(img, 1)

        # Track and revert the image
        track.find_hand(flip_image)
        pos_list_dict = track.find_finger_tips(
            flip_image,
            finger_list=None,  # Add Finger string list else None
            show_connected=True,
            show_landmarks=True,
            draw_tips=False,
            hand_id_list=[0]
        )
        # Get all Landmarks
        pos_list_dict = track.find_all_landmarks(
            flip_image,
            hand_id_list=[0],
            finger_list=None
        )
        lms_list = pos_list_dict['0']
        total = 0
        tip_list = [8, 12, 16, 20]
        if len(lms_list) != 0:
            total = sum([lms_list[finger][1] < lms_list[finger - 1][1] for finger in tip_list])
            total += lms_list[4][0] < lms_list[3][0]

        cv2.putText(flip_image, "{}".format(total), (550, 100), cv2.FONT_HERSHEY_PLAIN, 7, (0, 0, 255), 6)
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


if __name__ == "__main__":
    main(show_fps=True)
