try:
    import sys
    import cv2
    import time
    import math
    import pandas as pd
    import utils.hand_tracking as ht
except ModuleNotFoundError:
    sys.path.append("../")
finally:
    import utils.hand_tracking as ht


def pre_process(landmarks):
    flatten = []
    for lms in landmarks:
        for point in lms:
            flatten.append(point)
    return flatten


def main(show_fps=False, video_src=0, flip: bool = True, csv_src: str = 'record.csv', sample=100):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    cap.set(3, 1280)
    cap.set(4, 740)
    previous_time = 0
    track = ht.HandTracking(min_detection_confidence=0.8,
                            min_tracking_confidence=0.8)
    is_record = True
    while is_record:
        temp = sample
        label = input("Enter Label: ")

        # Infinite loop waiting for key 'q' to terminate
        while cv2.waitKey(1) and temp > 0:
            # # Read the frame
            success, img = cap.read()
            # # Flip input image horizontally
            flip_image = cv2.flip(img, 1) if flip else img

            # Track and revert the image
            track.find_hand(flip_image)
            finger_up_dict = track.find_raw_landmarks(hand_id_list=[0])
            if len(finger_up_dict['0']):
                temp -= 1
                flatten = pre_process(finger_up_dict['0'])
                print(flatten)
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
        is_record = input("Do you want to record? (y/n)")
        is_record = is_record.upper() == 'Y'


if __name__ == "__main__":
    main(show_fps=True)
