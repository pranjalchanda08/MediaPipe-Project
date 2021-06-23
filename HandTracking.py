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
        # Make a dictionary of landmarks with its index
        self.LM_DICT = {lm:HandTracking.LANDMARK.index(lm) for lm in HandTracking.LANDMARK}
        # Load the hand model
        self.mpHand = mp.solutions.hands
        # Load mediapipe drawing utility
        self.mpDraw = mp.solutions.drawing_utils
        # Create hand object
        self.hands  = self.mpHand.Hands(
            static_image_mode        ,
            max_num_hands            ,
            min_detection_confidence ,
            min_tracking_confidence
            )

    def findFingerTips( self, 
                        imgBGR, 
                        color=(255,255,255), 
                        showConnected=False,
                        showLandmarks=False,
                        Finger_list=None
                       ):
        '''
            Finds finger tips location on cv2.BGR image
        '''
        Finger_points = [
                        self.LM_DICT['THUMB_TIP'],
                        self.LM_DICT['INDEX_TIP'],
                        self.LM_DICT['MIDDLE_TIP'],
                        self.LM_DICT['RING_TIP'],
                        self.LM_DICT['PINKY_TIP']
                    ]
        cx , cy = None, None
        if Finger_list is not None:
            Finger_points = [self.LM_DICT[(finger.upper()+'_TIP')] for finger in Finger_list]

        # Convert the image to RGB
        imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
        # Process the RGB image using the model
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            # Itterate over all landmarks
            for landmarks in results.multi_hand_landmarks:
                for index_, lm in enumerate(landmarks.landmark):
                    # Get the height and width of image
                    h, w, c = imgBGR.shape
                    # Calculate the position of the landmark in the picture
                    cx , cy = int(w * lm.x), int(h * lm.y)
                    # Check if the landmark is present in the index list
                    if index_ in Finger_points:
                        # Draw circles around the detections
                        cv2.circle(imgBGR, (cx,cy), 15, color, cv2.FILLED)
                # Draw the landmark points on image
                if showLandmarks:
                    self.mpDraw.draw_landmarks(
                        imgBGR,
                        landmarks,
                        self.mpHand.HAND_CONNECTIONS if showConnected else None
                        )

        return cx,cy    