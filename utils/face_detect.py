try:
    import cv2
    import mediapipe as mp
    import time
except ModuleNotFoundError:
    print("Install required packages")


class FaceDetect:
    def __init__(
            self,
            min_detection_confidence=0.8,
            model_selection=0
    ):
        self.results = None
        # Load face detection module
        self.mp_face = mp.solutions.face_detection
        # Load media-pipe drawing utility
        self.mp_draw = mp.solutions.drawing_utils
        # Load Face detection model
        self.face = self.mp_face.FaceDetection(min_detection_confidence=min_detection_confidence,
                                               model_selection=model_selection)

    def detect_faces(self, img_bgr):
        # Convert image to RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # get Process results
        self.results = self.face.process(img_rgb)

    def get_lms(self, img_bgr, draw=False):
        ret_dict = {'keyPoints': []}
        if self.results.detections:
            for index_, detection in enumerate(self.results.detections):
                cord_list = []
                for key_point in detection.location_data.relative_keypoints:
                    h, w, c = img_bgr.shape
                    cord_list.append((int(w * key_point.x), int(h * key_point.y)))
                if draw:
                    self.mp_draw.draw_detection(img_bgr, detection)
                ret_dict['keyPoints'].append(cord_list)
        return ret_dict


def main(show_fps=False, video_src: str = 0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    detect = FaceDetect()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(20) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        if not success:
            break
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1)
        detect.detect_faces(flip_image)
        ret = detect.get_lms(flip_image, draw=True)
        print(ret)
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
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_list = ['face1']
    for video in video_list:
        main(show_fps=True, video_src="../gallery/Inputs/Video/{}.mp4".format(video))
