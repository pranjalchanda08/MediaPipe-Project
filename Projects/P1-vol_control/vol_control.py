try:
    import sys
    import cv2
    import time
    import math
    import alsaaudio
    import numpy as np
    import utils.hand_tracking as ht
except Exception:
    sys.path.append("../../")
finally:
    import utils.hand_tracking as ht


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def vector_len(a_tup, b_tup):
    return int(math.hypot(a_tup[0] - b_tup[0], a_tup[1] - b_tup[1]))


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
        pos_list_dict = track.find_finger_tips(
            flip_image,
            finger_list=None,  # Add Finger string list else None
            show_connected=True,
            show_landmarks=True,
            draw_tips=True,
            hand_id_list=[0]
        )
        # Get all Landmarks
        pos_list_dict = track.find_all_landmarks(
            flip_image,
            hand_id_list=[0],
            finger_list=None
        )
        # get current volume
        vol = audio.getvolume()
        # Process the landmark
        if len(pos_list_dict['0']) != 0:
            # Get position indexes
            (x_thumb_tip, y_thumb_tip) = (pos_list_dict['0'][track.LM_DICT['THUMB_TIP']])
            (x_index_tip, y_index_tip) = (pos_list_dict['0'][track.LM_DICT['INDEX_TIP']])
            (x_middle, y_middle) = (pos_list_dict['0'][track.LM_DICT['MIDDLE_TIP']])
            (x_ring, y_ring) = (pos_list_dict['0'][track.LM_DICT['RING_TIP']])
            (x_pinky, y_pinky) = (pos_list_dict['0'][track.LM_DICT['PINKY_TIP']])
            (x_wrist, y_wrist) = (pos_list_dict['0'][track.LM_DICT['WRIST']])
            # Draw line between Thumb and Index tip
            cv2.line(flip_image, (x_thumb_tip, y_thumb_tip), (x_index_tip, y_index_tip), (0, 0, 255), 3)
            # Get vector lengths between landmarks
            dis_thumb_index = vector_len((x_thumb_tip, y_thumb_tip), (x_index_tip, y_index_tip))
            dis_wrist_middle = vector_len((x_wrist, y_wrist), (x_middle, y_middle))
            dis_wrist_ring = vector_len((x_wrist, y_wrist), (x_ring, y_ring))
            dis_wrist_pinky = vector_len((x_wrist, y_wrist), (x_pinky, y_pinky))

            print("Volume {}, Distance Middle: {}, Ring: {}, Pinky: {}".format(vol[0],
                                                                               dis_wrist_middle,
                                                                               dis_wrist_ring,
                                                                               dis_wrist_pinky))
            if (0 <= dis_wrist_middle <= 100) and (0 <= dis_wrist_ring <= 80) and (0 <= dis_wrist_pinky <= 90):
                if dis_thumb_index < 30:
                    mapped = 0
                elif dis_thumb_index > 220:
                    mapped = 100
                else:
                    mapped = int(np.interp(dis_thumb_index, [30, 220], [0, 100]))
                if 0 <= mapped <= 100:
                    audio.setvolume(mapped)
        vol_bar = int(np.interp(vol[0], [0, 100], [400, 150]))
        cv2.rectangle(flip_image, (50, 150), (85, 400), (0, 255, 0), 5)
        cv2.rectangle(flip_image, (51, vol_bar), (84, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(flip_image, "Vol: {}%".format(vol[0]), (40, 140), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
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
