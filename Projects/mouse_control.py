try:
    import sys
    import cv2
    import time
    import math
    import pyautogui
    import numpy as np
    import utils.hand_tracking as ht
except ModuleNotFoundError:
    sys.path.append("../")
finally:
    import utils.hand_tracking as ht


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    track = ht.HandTracking(min_detection_confidence=0.7)
    screen_width, screen_height = pyautogui.size()
    cap.set(3, screen_width)
    cap.set(4, screen_height)

    w_box, h_box = 640, 400
    frame_offset = 150
    pyautogui.FAILSAFE = False
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1)
        h, w, c = flip_image.shape
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
        finger_up_dict = track.is_finger_up(flip_image, hand_id_list=[0])
        finger_up = finger_up_dict['0']
        # if index is up
        pt1_x, pt1_y = (w - frame_offset, 0)
        pt2_x, pt2_y = (w - (w_box + frame_offset), h_box)
        cv2.rectangle(flip_image, (pt1_x, pt1_y), (pt2_x, pt2_y), (255, 0, 255), 2)
        if len(finger_up):
            landmarks = finger_up_dict['lms']
            if finger_up[0] and sum(finger_up) == 1:
                finger_pos = landmarks['0'][8][:2]
                abs_x = round(np.interp(finger_pos[0] - pt2_x, [0.0, 640], [0.0, 1.0]), 2)
                abs_y = round(np.interp(finger_pos[1] - pt1_y, [0.0, 400], [0.0, 1.0]), 2)
                pyautogui.moveTo(screen_width * abs_x, screen_height * abs_y)

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
    main()
