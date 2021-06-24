import cv2
import time
import HandTracking as ht


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    current_time = 0
    fps = 0
    track = ht.HandTracking()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        # Flip input image horizontally
        flipimage = cv2.flip(img, 1)

        # Track and revert the image
        track.find_hand(flipimage)
        pos_list_dict = track.find_finger_tips(
            flipimage,
            finger_list=None,  # Add Finger string list else None
            show_connected=True,
            show_landmarks=True,
            draw_tips=True,
            hand_id_list=[0, 1]
        )
        pos_list_dict = track.find_all_landmarks(
            flipimage,
            hand_id_list=[0, 1],
            finger_list=None
        )
        print(pos_list_dict)
        # Calculate FPS
        if show_fps:
            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time
            # Include FPS text in image
            cv2.putText(flipimage,
                        "FPS: {}".format(int(fps)),
                        (10, 70),  # Position
                        cv2.FONT_HERSHEY_PLAIN,
                        1,  # Font size
                        (0, 0, 255),
                        2  # Thickness
                        )
        # Show the resultant image
        cv2.imshow("Output", flipimage)


if __name__ == '__main__':
    main(show_fps=True)
