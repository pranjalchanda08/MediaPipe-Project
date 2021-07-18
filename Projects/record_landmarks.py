try:
    import sys
    import cv2
    import time
    import math
    import pandas as pd
    import utils.hand_tracking as ht
except ModuleNotFoundError:
    sys.path.append("../")
finally:
    import utils.hand_tracking as ht


def flatten(landmarks):
    flat = []
    for lms in landmarks:
        for point in lms:
            flat.append(point)
    return flat


def main(show_fps=False,
         video_src=0,
         flip: bool = True,
         csv_src: str = 'record.csv',
         write_mode='w',
         sample_per_label=100):
    # Capture the video stream Webcam
    cap = cv2.VideoCapture(video_src)
    cap.set(3, 1280)
    cap.set(4, 740)
    previous_time = 0
    track = ht.HandTracking(min_detection_confidence=0.8,
                            min_tracking_confidence=0.8)
    is_record = True
    columns = []
    for i in range(0, 21):
        for x in ['_x', '_y', '_z']:
            columns.append((str(i) + x))
    columns.append('labels')
    print(columns)
    array_entry = []
    while is_record:
        temp = sample_per_label
        label = input("Enter Label: ")

        # Infinite loop waiting for key 'q' to terminate
        while cv2.waitKey(1) and temp > 0:
            # # Read the frame
            success, img = cap.read()
            if not success:
                continue
            # Flip input image horizontally
            flip_image = cv2.flip(img, 1) if flip else img

            # Track and revert the image
            track.find_hand(flip_image)
            finger_up_dict = track.find_raw_landmarks(flip_image,
                                                      hand_id_list=[0],
                                                      show_connected=True,
                                                      show_landmarks=True)
            if len(finger_up_dict['0']):
                temp -= 1
                flat = flatten(finger_up_dict['0'])
                flat.append(label)
                array_entry.append(flat)

            # Calculate FPS
            if show_fps:
                current_time = time.time()
                fps = 1 / (current_time - previous_time)
                previous_time = current_time
                cv2.putText(flip_image, "FPS: {}".format(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            # Show the resultant image
            cv2.imshow("Output", flip_image)
        is_record = input("Do you want to record more? (y/n)")
        is_record = is_record.upper() == 'Y'
    data_frame = pd.DataFrame(array_entry, columns=columns)
    data_frame.to_csv(csv_src, mode=write_mode)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    samples = int(input("Enter number of samples per label: "))
    append = input("Wish to append previous records? (y/n) ")
    append = 'a' if append.upper() == 'Y' else 'w'
    main(
        show_fps=True,
        video_src=0,
        flip=True,
        csv_src='record.csv',
        sample_per_label=samples,
        write_mode=append
    )
