try:
    import sys
    import cv2
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
    cap.set(4, 740)
    previous_time = 0
    track = ht.HandTracking(min_detection_confidence=0.8,
                            min_tracking_confidence=0.8)

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
        finger_up_dict = track.is_finger_up(flip_image, hand_id_list=[0])
        finger_list = finger_up_dict['0']
        # Index Up - Draw Mode
        if sum(finger_list) == 1 and finger_list[1]:
            pass
        # Index and Middle up - Move mode
        elif sum(finger_list) == 2 and finger_list[1] and finger_list[2]:
            pass
        # All up except thumb - erase mode
        elif sum(finger_list) == 4 and not finger_list[0]:
            pass
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
