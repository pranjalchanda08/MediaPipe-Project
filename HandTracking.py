import cv2
import mediapipe as mp
import time

class HandTracking():
    LANDMARK = [
        'WRIST',
        'THUMB_CMC',    'THUMP_MCP',    'THUMB_IP',     'THUMB_TIP',
        'INDEX_MCP',    'INDEX_PIP',    'INDEX_DIP',    'INDEX_TIP',
        'MIDDLE_MCP',   'MIDDLE_PIP',   'MIDDLE_DIP',   'MIDDLE_TIP',
        'RING_MCP',     'RING_PIP',     'RING_DIP',     'RING_TIP',
        'PINKY_MCP',    'PINKY_PIP',    'PINKY_DIP',    'PINKY_TIP'
    ]

    def __init__(
                self,
                static_image_mode        = False,     # If True the whole time it will perform detection
                max_num_hands            = 4,
                min_detection_confidence = 0.7,
                min_tracking_confidence  = 0.7
                ):
        '''
            Initializes the HandTracking module
        '''
        self.results = None
        # Make a dictionary of landmarks with its index
        self.LM_DICT = {lm:HandTracking.LANDMARK.index(lm) for lm in HandTracking.LANDMARK}
        # Load the hand_landmarks model
        self.mpHand = mp.solutions.hands
        # Load mediapipe drawing utility
        self.mpDraw = mp.solutions.drawing_utils
        # Create hand_landmarks object
        self.hands  = self.mpHand.Hands(
            static_image_mode        ,
            max_num_hands            ,
            min_detection_confidence ,
            min_tracking_confidence
            )

    def findHand( self,
                  imgBGR,
                ):
        # Convert the image to RGB
        imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
        # Process the RGB image using the model
        self.results = self.hands.process(imgRGB)


    def findFingerTips( self,
                        imgBGR,
                        color           = (255,255,255),
                        show_connected  = False,
                        show_landmarks  = False,
                        draw_tips       = True,
                        finger_list     = None,
                        hand_id_list    = 0
                       ):
        '''
            Finds finger tips location on cv2.BGR image
        '''
        try:
            Finger_points = \
                [
                    self.LM_DICT['THUMB_TIP'],
                    self.LM_DICT['INDEX_TIP'],
                    self.LM_DICT['MIDDLE_TIP'],
                    self.LM_DICT['RING_TIP'],
                    self.LM_DICT['PINKY_TIP']
                ]
            cx , cy = None, None
            return_dict = {str(hand_id) : [] for hand_id in hand_id_list}
            if finger_list is not None:
                Finger_points = [self.LM_DICT[(finger.upper()+'_TIP')] for finger in finger_list]

            if self.results.multi_hand_landmarks:
                # Itterate over all hands
                for hand_id in hand_id_list:
                    return_dict[str(hand_id)] = []
                    hand_landmarks = self.results.multi_hand_landmarks [ hand_id ]
                    for index_, lm in enumerate(hand_landmarks.landmark):
                        # Get the height and width of image
                        h, w, c = imgBGR.shape
                        # Calculate the position of the landmark in the picture
                        cx , cy = int(w * lm.x), int(h * lm.y)
                        # Check if the landmark is present in the index list
                        if index_ in Finger_points:
                            # Append the x,y coordinates  of the landmark
                            return_dict[str(hand_id)].append((cx, cy)) 
                            # Draw circles around the detections
                            cv2.circle(imgBGR, (cx,cy), 15, color, cv2.FILLED) if draw_tips else None
                    # Draw the landmark points on image
                    if show_landmarks:
                        self.mpDraw.draw_landmarks(
                            imgBGR,
                            hand_landmarks,
                            self.mpHand.HAND_CONNECTIONS if show_connected else None
                            )
        except :
            pass
        finally:
            return return_dict

    def findAllLandmarks(
                        self,
                        imgBGR,
                        hand_id_list    = 0,
                        finger_list     = None
                    ):
        try:
            cx , cy = None, None
            return_dict = {str(hand_id) : [] for hand_id in hand_id_list}
            if finger_list is not None:
                Finger_points = [self.LM_DICT[(finger.upper()+'_TIP')] for finger in finger_list]

            if self.results.multi_hand_landmarks:
                # Itterate over all hands
                for hand_id in hand_id_list:
                    return_dict[str(hand_id)] = []
                    hand_landmarks = self.results.multi_hand_landmarks [ hand_id ]
                    for index_, lm in enumerate(hand_landmarks.landmark):
                        # Get the height and width of image
                        h, w, c = imgBGR.shape
                        # Calculate the position of the landmark in the picture
                        cx , cy = int(w * lm.x), int(h * lm.y)
                        # Check if the landmark is present in the index list
                        # Append the x,y coordinates  of the landmark
                        return_dict[str(hand_id)].append((cx, cy)) 
        except :
            pass
        finally:
            return return_dict