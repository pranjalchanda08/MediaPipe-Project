import time
import cv2
import mediapipe as mp


class PoseEstimation:
    def __init__(
            self,
            static_image_mode=False,
            model_complexity=2,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
    ):
        """
        Initialise pose estimation
            :param static_image_mode:
            :param model_complexity:
            :param smooth_landmarks:
            :param min_detection_confidence:
            :param min_tracking_confidence:
        """
        self.results = None
        # Load pose model from media-pipe
        self.mp_pose = mp.solutions.pose
        # Load media-pipe drawing utility
        self.mp_draw = mp.solutions.drawing_utils
        # Create pose landmark object
        self.pose = self.mp_pose.Pose(
            static_image_mode,
            model_complexity,
            smooth_landmarks,
            min_detection_confidence,
            min_tracking_confidence
        )
        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=1,
                                                     circle_radius=1,
                                                     color=mp.solutions.drawing_utils.BLUE_COLOR)

    def find_body(self, img_bgr):
        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # Process the input image
        self.results = self.pose.process(img_rgb)

    def find_lms(self, img_bgr):
        if self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(img_bgr,
                                        self.results.pose_landmarks,
                                        self.mp_pose.POSE_CONNECTIONS,
                                        self.drawing_spec)


def main(show_fps=False, video_src=0):
    cap = cv2.VideoCapture(video_src)
    previous_time = 0
    body_lms = PoseEstimation()
    while cv2.waitKey(1) != (ord('q') or ord('Q')):
        success, img = cap.read()
        if not success:
            print("read_err")
            break
        # Flip input image horizontally
        flip_image = cv2.flip(img, 1)

        body_lms.find_body(flip_image)
        body_lms.find_lms(flip_image)
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


if __name__ == "__main__":
    video_list = ['pose1']
    for video in video_list:
        main(show_fps=True, video_src="../gallery/Inputs/Video/{}.mp4".format(video))
