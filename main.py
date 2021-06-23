import cv2
import HandTracking as ht

def main():    
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(0)

    track = ht.HandTracking()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        # Flip input image horizontally
        flipImage = cv2.flip(img, 1)
        # Track and revert the image
        track.findHands(flipImage, showFps = True)
        # Show the resultant image
        cv2.imshow("Output", flipImage)

if __name__ == '__main__':
    main()