import cv2
import mediapipe as mp
import time

# List of available landmarks
LANDMARK = [
    'WRIST',        
    'THUMB_CMC',    'THUMP_MCP',    'THUMB_IP',     'THUMB_TIP',
    'INDEX_MCP',    'INDEX_PIP',    'INDEX_DIP',    'INDEX_TIP',
    'MIDDLE_MCP',   'MIDDLE_PIP',   'MIDDLE_DIP',   'MIDDLE_TIP',
    'RING_MCP',     'RING_PIP',     'RING_DIP',     'RING_TIP',
    'PINKY_MCP',    'PINKY_PIP',    'PINKY_DIP',    'PINKY_TIP'
]

# Make a dictionary of landmarks with its index
LM_DICT = {lm:LANDMARK.index(lm) for lm in LANDMARK}

# Capture the video stream Webcam
cap = cv2.VideoCapture(0)

# Load the hand model
mpHand = mp.solutions.hands
# Load mediapipe drawing utility
mpDraw = mp.solutions.drawing_utils
# Create hand object
hands = mpHand.Hands(
    static_image_mode        = False,     # If True the whole time it will perform detection
    max_num_hands            = 4,
    min_detection_confidence = 0.7,
    min_tracking_confidence  = 0.7
    )

fps   = 0
ctime = 0
ptime = 0

# Infinite loop waiting for key 'q' to terminate
while cv2.waitKey(1) != (ord('q') or ord('Q')):

    # Read the frame
    success, img = cap.read()
    # Flip input image horizontally
    flipImage = cv2.flip(img, 1)
    # Convert the image to RGB
    imgRGB = cv2.cvtColor(flipImage, cv2.COLOR_BGR2RGB)
    # Process the RGB image using the model
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
    # Itterate over all landmarks
        for landmarks in results.multi_hand_landmarks:
            for index_, lm in enumerate(landmarks.landmark):
                # Get the height and width of image
                h, w, c = flipImage.shape
                # Calculate the position of the landmark in the picture
                cx , cy = int(w * lm.x), int(h * lm.y)
                # Check if the landmark is present in the index list
                if index_ in [
                    LM_DICT['WRIST'],
                    LM_DICT['THUMB_TIP'], 
                    LM_DICT['INDEX_TIP'], 
                    LM_DICT['MIDDLE_TIP'], 
                    LM_DICT['RING_TIP'], 
                    LM_DICT['PINKY_TIP']
                ]:
                # Draw circles around the detections
                    cv2.circle(flipImage, (cx,cy), 15, (255,0,255), cv2.FILLED)

            # Draw the landmark points on image
            mpDraw.draw_landmarks(
                flipImage, 
                landmarks, 
                mpHand.HAND_CONNECTIONS
                )
    # Calculate FPS
    ctime = time.time()
    fps   = 1/(ctime - ptime)
    ptime = ctime 

    # Include FPS text in image
    cv2.putText(flipImage, 
        "FPS: {}".format(int(fps)), 
        (10,70),                        # Position
        cv2.FONT_HERSHEY_PLAIN,
        1,                              # Font size
        (0,255,0),
        1                               # Thickness
        )
    cv2.imshow("Output", flipImage)