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
- [ ] Pose Estimation

![HT](gallery/Output/ht.gif)

![face](gallery/Output/face.gif)

## Projects

* ### P1: Hand Gesture based system volume control
  **Objective:**
  
    Real time volume control using hand gesture. The volume of the system shall be controlled only when middle, ring and
  pinky fingers are closed.
    ```shell
    cd MediaPipe-Project/Projects/P1-vol_control
    python3 vol_control.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04
  
    ![hc1](gallery/Output/VolC.gif)
  
* ### P2: Finger Counter
  **Objective:**  

  Real time finger counting.
    ```shell
    cd MediaPipe-Project/Projects/P2-finger_counting
    python3 finger_counter.py
    ```
  **Compatibility**:
    - [X] Windows 10
    - [X] Ubuntu 20.04
  
    ![fc1](gallery/Output/FC.gif) 
  

## Reference

* [Mediapipe](https://google.github.io/mediapipe/)
* [OpenCV](https://pypi.org/project/opencv-python/)
* [pycaw](https://github.com/AndreMiras/pycaw)
* [alsaaudio](https://pypi.org/project/pyalsaaudio/)
