# Mediapipe Projects

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![opencv](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![TF](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Pcharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)

A set of project using OpenCV and Media Pipe library.

## System Requirements  


* Ubuntu 20.04
* Python 3.8.5
* **No GPU** requirements

## Installation

* ### Ubuntu 20.04
  ```sh
  $ pip3 install -r requirements_linux.txt
  ```
* ### Windows 10
  ```shell
  /> pip3 install -r requirements_win.txt
  ```  

## Utilities

- [X] Hand Tracking
- [X] Face Detection
- [X] Face Mesh
- [X] Pose Estimation
- [X] Objectron (3D Object Detection)

### Hand Landmark:

![HT](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/ht.gif?raw=true)

### Face Detection:

![face](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/face.gif?raw=true)

### Face Mesh:

![faceMesh](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/face_mesh.gif?raw=true)

### Pose Estimation:

![Pose](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/pose_est.gif?raw=true)

### Objectron:

![Pose](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/obj.gif?raw=true)
## Projects

* ### P1: Hand Gesture based system volume control
  **Objective:**

  Real time volume control using hand gesture. The volume of the system shall be controlled only when middle, ring and
  pinky fingers are closed.
    ```shell
    python3 vol_control.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04

  ![hc1](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/VolC.gif?raw=true)

* ### P2: Finger Counter
  **Objective:**

  Real time finger counting.
    ```shell
    python3 finger_counter.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04

  ![fc1](https://github.com/pranjalchanda08/MediaPipe-Project/blob/master/gallery/Output/FC.gif?raw=true)
* ### P3: Finger Mouse control
  **Objective:**

  To control mouse pointer using finger tracking.
    1. Use Index finger only to move the cursor
    2. Use Index and Middle fingers to do left-click
    3. Use Index, Middle and Ring to do right-click
    4. Perform step-ii twice fast for double click

    ```shell
    python3 mouse_control.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04
  
* ### P4: Finger Virtual Painter
  **Objective:**

  To Paint on the screen using finger gestures.
    1. Use 👆 to Draw
    2. Use 🤚 to Erase
    3. Make a 🤟 to clear the screen

    ```shell
    python3 finger_painter.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04

## Known issues:
1. Segmentation Fault due to keypress in OpenCV when using with Ubuntu 20.04. [OpenCV Github Issue #20311](https://github.com/opencv/opencv/issues/20311)
## Reference

* [Mediapipe](https://google.github.io/mediapipe/)
* [OpenCV](https://pypi.org/project/opencv-python/)
* [pycaw](https://github.com/AndreMiras/pycaw)
* [alsaaudio](https://pypi.org/project/pyalsaaudio/)
* [pyautogui](https://pypi.org/project/pyautogui/)
