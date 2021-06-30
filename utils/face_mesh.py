try:
    import cv2
    import mediapipe as mp
    import time
except ModuleNotFoundError:
    print("Install required packages")


class FaceMesh:
    def __init__(self,
                 static_image_mode=False,
                 max_num_faces=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5
                 ):
        self.ctr = 0
        self.results = None
        # Load face detection module
        self.mp_face = mp.solutions.face_mesh
        # Load media-pipe drawing utility
        self.mp_draw = mp.solutions.drawing_utils
        # Load Face detection model
        self.face = self.mp_face.FaceMesh(static_image_mode,
                                          max_num_faces,
                                          min_detection_confidence,
                                          min_tracking_confidence
                                          )
        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=1,
                                                     circle_radius=1,
                                                     color=mp.solutions.drawing_utils.BLUE_COLOR)
        self.connect_spec = self.mp_draw.DrawingSpec(thickness=1,
                                                     circle_radius=1,
                                                     color=mp.solutions.drawing_utils.BLACK_COLOR)

    def find_face(self, img_bgr):
        # Convert image to RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # get Process results
        self.results = self.face.process(img_rgb)

    def find_face_landmarks(self, img_bgr):
        ret_list = []
        if self.results.multi_face_landmarks:
            h, w, c = img_bgr.shape
            for face_landmarks in self.results.multi_face_landmarks:
                for idx, landmark in enumerate(face_landmarks.landmark):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    ret_list.append((cx, cy))
                self.mp_draw.draw_landmarks(
                    image=img_bgr,
                    landmark_list=face_landmarks,
                    connections=self.mp_face.FACE_CONNECTIONS,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.connect_spec
                )
        return ret_list


def main(show_fps=False, video_src=0):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    detect = FaceMesh()
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(20) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        if not success:
            break
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1)
        detect.find_face(flip_image)
        ret = detect.find_face_landmarks(flip_image)
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
