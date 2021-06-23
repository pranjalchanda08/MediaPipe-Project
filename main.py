import cv2
import mediapipe as mp
import time

# Capture the video stream Webcam
cap = cv2.VideoCapture(0)

# Load the hand model
mpHand = mp.solutions.hands

# Load mediapipe drawing utility
mpDraw = mp.solutions.drawing_utils

hands = mpHand.Hands(
	static_image_mode        = False,     # If True the whole time it will perform detection
	max_num_hands            = 2,
	min_detection_confidence = 0.5,
	min_tracking_confidence  = 0.7
	)

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
	# Print landmarks
	# print(results.multi_hand_landmarks)
	
	if results.multi_hand_landmarks:
	# Itterate over all landmarks
		for landmarks in results.multi_hand_landmarks:
			# Draw the landmark points on image
			mpDraw.draw_landmarks(flipImage, landmarks)

	cv2.imshow("Output", flipImage)