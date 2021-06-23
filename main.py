import cv2
import mediapipe as mp
import time

# Capture the video stream Webcam
cap = cv2.VideoCapture(0)

# Load the model
mpHand = mp.solutions.hands

hands = mpHand.Hands(
	static_image_mode        = False,     # If True the whole time it will perform detection
	max_num_hands            = 2,
	min_detection_confidence = 0.5,
	min_tracking_confidence  = 0.7
	)
while cv2.waitKey(1) != ord('q'):
	
	# Read the frame
	success, img = cap.read()
	# Convert the image to RGB
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# Process the RGB image using the model
	results = hands.process(imgRGB)
	# Print landmarks
	print(results.multi_hand_landmarks)
	
	cv2.imshow("Capture", img)