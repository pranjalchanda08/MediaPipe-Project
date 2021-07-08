try:
    import cv2
    import mediapipe as mp
    import time
except ModuleNotFoundError:
    print("Install required packages")

SHOE = 'Shoe'
CHAIR = 'Chair'
CUP = 'Cup'
CAMERA = 'Camera'


class Objectron:
    def __init__(self,
                 static_image_mode=True,
                 max_num_objects=5,
                 min_detection_confidence=0.5,
                 model_name: str = SHOE
                 ):
        self.result = None
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_obj = mp.solutions.objectron
        self.object = self.mp_obj.Objectron(
            static_image_mode=static_image_mode,
            max_num_objects=max_num_objects,
            min_detection_confidence=min_detection_confidence,
            model_name=model_name
        )
        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=2,
                                                     circle_radius=1,
                                                     color=mp.solutions.drawing_utils.BLUE_COLOR)
        self.connect_spec = self.mp_draw.DrawingSpec(thickness=2,
                                                     circle_radius=1,
                                                     color=(255, 255, 255))

    def find_object(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2BGR)
        self.result = self.object.process(img_rgb)

    def get_landmarks(self, img_bgr, draw: bool = True):
        ret_list = []
        if self.result.detected_objects:
            h, w, c = img_bgr.shape
            for detected_object in self.result.detected_objects:
                for idx, landmark in enumerate(detected_object.landmarks_2d.landmark):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    ret_list.append((cx, cy))
                if draw:
                    self.mp_draw.draw_landmarks(
                        image=img_bgr,
                        landmark_list=detected_object.landmarks_2d,
                        connections=self.mp_obj.BOX_CONNECTIONS,
                        landmark_drawing_spec=self.drawing_spec,
                        connection_drawing_spec=self.connect_spec
                    )
        return ret_list


def main(show_fps=False, video_src: str = 0, flip: bool = False, model_name: str = SHOE):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    detect = Objectron(model_name=model_name)
    # Infinite loop waiting for key 'q' to terminate
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        # Read the frame
        success, img = cap.read()
        if not success:
            break
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1) if flip else img
        detect.find_object(flip_image)
        ret = detect.get_landmarks(flip_image)
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
    video_list = ['shoe1', 'shoe2']
    for video in video_list:
        main(show_fps=True, video_src="../gallery/Inputs/Video/{}.mp4".format(video))
    video_list = ['cup1', 'cup2']
    for video in video_list:
        main(show_fps=True, video_src="../gallery/Inputs/Video/{}.mp4".format(video), model_name=CUP)
