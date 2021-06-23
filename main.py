import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

while cv2.waitKey(1) != ord('q'):
	success, img = cap.read()
	cv2.imshow("Capture", img)