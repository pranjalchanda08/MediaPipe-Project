import cv2
import time
import HandTracking as ht

def main( showFps = False ):    
    # Capture the video stream Webcam
    cap   = cv2.VideoCapture(0)
    ptime = 0
    ctime = 0
    fps   = 0
    track = ht.HandTracking()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        # Flip input image horizontally
        flipImage = cv2.flip(img, 1)
        # Track and revert the image
        ctime = time.time()
        cx,cy = track.findFingerTips(flipImage, 
                                    Finger_list = None
                                    ) # Add Finger string list else None
        # Calculate FPS
        if showFps:
            ctime = time.time()
            fps   = 1/(ctime - ptime)
            ptime = ctime
            # Include FPS text in image
            cv2.putText(flipImage,
                "FPS: {}".format(int(fps)),
                (10,70),                        # Position
                cv2.FONT_HERSHEY_PLAIN,
                1,                              # Font size
                (0,0,255),
                2                               # Thickness
                )
        # Show the resultant image
        cv2.imshow("Output", flipImage)

if __name__ == '__main__':
    main(showFps = True)