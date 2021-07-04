try:
    import sys
    from cv2 import cv2
    import numpy as np
    import time
    import math
    import utils.hand_tracking as ht
except ModuleNotFoundError:
    sys.path.append("../")
finally:
    import utils.hand_tracking as ht


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    cap.set(3, 1280)
    cap.set(4, 720)
    previous_time = 0
    track = ht.HandTracking(min_detection_confidence=0.85,
                            min_tracking_confidence=0.7)
    x_draw, y_draw = 0, 0

    canvas = np.zeros((720, 1280, 3), np.uint8)

    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # # Read the frame
        success, img = cap.read()
        # # Flip input image horizontally
        flip_image = cv2.flip(img, 1)

        # Track and revert the image
        track.find_hand(flip_image)
        track.find_finger_tips(
            flip_image,
            finger_list=None,  # Add Finger string list else None
            show_connected=True,
            show_landmarks=True,
            draw_tips=False,
            hand_id_list=[0]
        )
        finger_up_dict = track.is_finger_up(flip_image, hand_id_list=[0], threshold=2)
        finger_list = finger_up_dict['0']
        if len(finger_list):
            finger_sum = sum(finger_list)
            landmarks = finger_up_dict['lms']
            # Index Up - Draw Mode
            if finger_sum == 1 and finger_list[1]:
                x, y = landmarks['0'][8][:2]
                cv2.circle(flip_image, (x, y), 15, (255, 0, 255), cv2.FILLED)
                if not x_draw and not y_draw:
                    x_draw, y_draw = x, y
                cv2.line(canvas, (x_draw, y_draw), (x, y), (255, 0, 255), 15)
                x_draw, y_draw = x, y
            # All Fingers except thumb - Erase mode
            elif finger_sum == 4 and not finger_list[0]:
                x1, y1 = landmarks['0'][12][:2]
                cv2.circle(flip_image, (x1, y1), 50, (255, 255, 255), cv2.FILLED)
                cv2.circle(canvas, (x1, y1), 50, (0, 0, 0), cv2.FILLED)
                if not x_draw and not y_draw:
                    x_draw, y_draw = x1, y1
                cv2.line(canvas, (x1, y1), (x_draw, y_draw), (0, 0, 0), 50)
                x_draw, y_draw = x1, y1
            # Yo - Clear All
            elif finger_sum == 3 and not finger_list[2] and not finger_list[3]:
                canvas = np.zeros((720, 1280, 3), np.uint8)
            # Move Mode
            else:
                x_draw, y_draw = 0, 0
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
        img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, img_gray = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        flip_image = cv2.bitwise_and(flip_image, img_gray)
        flip_image = cv2.bitwise_or(flip_image, canvas)
        cv2.imshow("Output", flip_image)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(show_fps=True)
