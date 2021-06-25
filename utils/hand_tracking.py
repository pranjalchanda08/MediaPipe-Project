import cv2
import time
import mediapipe as mp


class HandTracking:
    LANDMARK = [
        'WRIST',
        'THUMB_CMC', 'THUMP_MCP', 'THUMB_IP', 'THUMB_TIP',
        'INDEX_MCP', 'INDEX_PIP', 'INDEX_DIP', 'INDEX_TIP',
        'MIDDLE_MCP', 'MIDDLE_PIP', 'MIDDLE_DIP', 'MIDDLE_TIP',
        'RING_MCP', 'RING_PIP', 'RING_DIP', 'RING_TIP',
        'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
    ]

    def __init__(
            self,
            static_image_mode=False,  # If True the whole time it will perform detection
            max_num_hands=4,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
    ):
        """
            Initializes the HandTracking module
        """
        self.results = None
        # Make a dictionary of landmarks with its index
        self.LM_DICT = {lm: HandTracking.LANDMARK.index(lm) for lm in HandTracking.LANDMARK}
        # Load the hand_landmarks model
        self.mpHand = mp.solutions.hands
        # Load media-pipe drawing utility
        self.mpDraw = mp.solutions.drawing_utils
        # Create hand_landmarks object
        self.hands = self.mpHand.Hands(
            static_image_mode,
            max_num_hands,
            min_detection_confidence,
            min_tracking_confidence
        )

    def find_hand(self,
                  img_bgr,
                  ):
        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # Process the RGB image using the model
        self.results = self.hands.process(img_rgb)

    def find_finger_tips(self,
                         img_bgr,
                         color=(255, 255, 255),
                         show_connected=False,
                         show_landmarks=False,
                         draw_tips=True,
                         finger_list=None,
                         hand_id_list=0
                         ):
        """
            Finds finger tips location on cv2.BGR image
        """
        try:
            finger_points = \
                [
                    self.LM_DICT['THUMB_TIP'],
                    self.LM_DICT['INDEX_TIP'],
                    self.LM_DICT['MIDDLE_TIP'],
                    self.LM_DICT['RING_TIP'],
                    self.LM_DICT['PINKY_TIP']
                ]
            cx, cy = None, None
            return_dict = {str(hand_id): [] for hand_id in hand_id_list}
            if finger_list is not None:
                finger_points = [self.LM_DICT[(finger.upper() + '_TIP')] for finger in finger_list]

            if self.results.multi_hand_landmarks:
                # Iterate over all hands
                for hand_id in hand_id_list:
                    return_dict[str(hand_id)] = []
                    hand_landmarks = self.results.multi_hand_landmarks[hand_id]
                    for index_, lm in enumerate(hand_landmarks.landmark):
                        # Get the height and width of image
                        h, w, c = img_bgr.shape
                        # Calculate the position of the landmark in the picture
                        cx, cy = int(w * lm.x), int(h * lm.y)
                        # Check if the landmark is present in the index list
                        if index_ in finger_points:
                            # Append the x,y coordinates  of the landmark
                            return_dict[str(hand_id)].append((cx, cy))
                            # Draw circles around the detections
                            cv2.circle(img_bgr, (cx, cy), 15, color, cv2.FILLED) if draw_tips else None
                    # Draw the landmark points on image
                    if show_landmarks:
                        self.mpDraw.draw_landmarks(
                            img_bgr,
                            hand_landmarks,
                            self.mpHand.HAND_CONNECTIONS if show_connected else None
                        )
        except Exception:
            pass
        finally:
            return return_dict

    def find_all_landmarks(
            self,
            img_bgr,
            hand_id_list=0,
            finger_list=None
    ):
        try:
            cx, cy = None, None
            return_dict = {str(hand_id): [] for hand_id in hand_id_list}
            if finger_list is not None:
                finger_points = [self.LM_DICT[(finger.upper() + '_TIP')] for finger in finger_list]

            if self.results.multi_hand_landmarks:
                # Iterate over all hands
                for hand_id in hand_id_list:
                    return_dict[str(hand_id)] = []
                    hand_landmarks = self.results.multi_hand_landmarks[hand_id]
                    for index_, lm in enumerate(hand_landmarks.landmark):
                        # Get the height and width of image
                        h, w, c = img_bgr.shape
                        # Calculate the position of the landmark in the picture
                        cx, cy = int(w * lm.x), int(h * lm.y)
                        # Check if the landmark is present in the index list
                        # Append the x,y coordinates  of the landmark
                        return_dict[str(hand_id)].append((cx, cy))
        except Exception:
            pass
        finally:
            return return_dict


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    current_time = 0
    fps = 0
    track = HandTracking()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1)

        # Track and revert the image
        track.find_hand(flip_image)
        pos_list_dict = track.find_finger_tips(
            flip_image,
            finger_list=None,  # Add Finger string list else None
            show_connected=True,
            show_landmarks=True,
            draw_tips=True,
            hand_id_list=[0, 1]
        )
        pos_list_dict = track.find_all_landmarks(
            flip_image,
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


if __name__ == '__main__':
    main(show_fps=True)
