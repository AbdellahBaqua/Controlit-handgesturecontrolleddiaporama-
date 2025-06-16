======================================
Professor Gesture & Speech Control App
======================================

.. contents:: Table of Contents

Overview
========

This application provides a robust, hands-free method for controlling presentations. It uses computer vision and speech recognition to interpret a presenter's commands.

The system is designed to "lock on" to a specific person (the "professor") using facial recognition. Once the professor is identified, the application tracks their body pose to intelligently find and interpret hand gestures. A special gesture activates a voice control mode, allowing for vocal commands to navigate the presentation. This dual-modal approach ensures that the system only listens for commands from the designated presenter and only when they explicitly signal their intent.

Key Features
============

* **Presenter-Specific Activation**: Uses facial recognition to identify a designated presenter and only begins tracking them, ignoring other people in the frame.
* **Dynamic Region-of-Interest (ROI)**: After finding the presenter, it uses pose estimation to create a dynamic search area for hands, significantly improving performance and reducing false positives.
* **Gesture-Based Control**: Recognizes a set of pre-trained hand gestures to perform actions such as starting the presentation, pausing/playing media, or moving to the previous slide.
* **Voice Command Mode**: A specific hand gesture activates a temporary speech recognition mode, allowing the presenter to use voice commands like "next," "previous," and "quit."
* **Real-time Debug View**: An optional overlay that visualizes the face detection box, pose skeleton, hand landmarks, and current operational state for easy troubleshooting.
* **Data Logging Mode**: Includes functionality to capture and log new hand gesture data, allowing for easy expansion or customization of the gesture vocabulary.

Requirements
============

Hardware
--------

* A standard webcam.
* A microphone recognized by your operating system.

Software
--------

* Python 3.8+
* The following Python libraries. You can install them via pip:

    .. code-block:: bash

        pip install opencv-python mediapipe numpy pyautogui sounddevice vosk face-recognition torch

Setup and Installation
======================

1.  **Project Structure**: The script expects a specific directory layout for its models and assets. Ensure your project folder is organized as follows:

    .. code-block:: text

        /your_project_folder/
        |-- app.py  (script)
        |-- professor.jpg
        |-- vosk-model-small-en-us-0.15/
        |   |-- (Vosk model files...)
        |-- model/
        |   |-- keypoint_classifier/
        |   |   |-- keypoint_classifier_weights.pth
        |   |   |-- keypoint_classifier_label.csv
        |   |   |-- keypoint.csv (This will be created if you log new gestures)

2.  **Set Professor Image**:
    Place a clear, front-facing photograph of the designated presenter in the root of the project directory and name it ``professor.jpg``.

3.  **Download Vosk Speech Model**:
    * Download the Vosk model for your language (the script is pre-configured for "vosk-model-small-en-us-0.15"). You can find models on the `Vosk models page <https://alphacephei.com/vosk/models>`_.
    * Unzip the model and ensure the resulting folder is named ``vosk-model-small-en-us-0.15`` and is placed in the root of the project directory.

4.  **Place Gesture Model**:
    Ensure the pre-trained gesture classifier weights (``keypoint_classifier_weights.pth``) and the corresponding labels file (``keypoint_classifier_label.csv``) are located inside the ``model/keypoint_classifier/`` directory.

Usage
=====

Running the Application
-----------------------

Execute the script from your terminal:

.. code-block:: bash

    python app.py

The application will start, open a window showing the webcam feed, and begin searching for the professor.

Command-Line Arguments
----------------------

You can customize the camera settings using the following arguments:

* ``--device``: The integer ID for your camera device. Default is ``0``.
* ``--width``: The capture width for the camera frame. Default is ``960``.
* ``--height``: The capture height for the camera frame. Default is ``540``.
* ``--use_static_image_mode``: A flag to indicate usage with static images instead of a live video stream.
* ``--min_detection_confidence``: Minimum confidence value (``0.0`` to ``1.0``) for hand detection. Default is ``0.7``.
* ``--min_tracking_confidence``: Minimum confidence value (``0.0`` to ``1.0``) for hand tracking. Default is ``0.5``.

Controls and Commands
=====================

The system operates through a hierarchy of keyboard, gesture, and voice commands.

Keyboard Controls
-----------------

These controls are active while the OpenCV window is in focus.

* **`ESC`** or **`q`**: Shuts down the application.
* **`d`**: Toggles the debug view, which shows skeletons, tracking boxes, and status text.
* **`k`**: Switches to "Logging Key Point" mode to record new gestures.
* **`n`**: Switches back to "Normal" mode from logging mode.
* **`0` - `9`**: When in logging mode, press a number to assign the current gesture to that class label in ``keypoint.csv``.

Gesture Controls
----------------

When the application is tracking the professor, it will look for the following hand gestures.

.. note:: The specific gesture for each action depends on the trained ``keypoint_classifier_weights.pth`` model and the labels in ``keypoint_classifier_label.csv``. The following are common examples.

* **Activate Speech Mode (ID 0)**: A specific gesture (e.g., "Thumbs Up") enables voice control for 5 seconds.
* **Start Presentation (ID 1)**: A gesture (e.g., "Fist") sends an `F5` key press.
* **Play/Pause (ID 2)**: A gesture (e.g., "Open Palm") sends a `spacebar` key press.
* **Previous Slide (ID 3)**: A gesture (e.g., "Pointing Left") sends a `left arrow` key press.

A cooldown period of 1.5 seconds prevents a single gesture from being triggered multiple times in rapid succession.

Voice Controls
--------------

Voice control is only active for 5 seconds after being triggered by the corresponding gesture.

* **`"next"`** or **`"forward"`** or **`"right"`**: Triggers a `right arrow` key press to advance to the next slide.
* **`"previous"`** or **`"back"`** or **`"backward"`** or **`"left"`**: Triggers a `left arrow` key press to return to the previous slide.
* **`"quit"`** or **`"exit"`** or **`"close"`**: Triggers an `ESC` key press to exit the presentation view.

Operational Flow
================

The application follows a state-based logic to function efficiently.

1.  **Searching Professor**: On startup, the system scans the entire camera frame at a reduced resolution to find a face that matches ``professor.jpg``. The status "INITIAL SEARCH" is shown.

2.  **Tracking Professor**: Once the professor is found, the system switches to tracking mode. It uses the detected face location to define a large Region of Interest (ROI) around the professor's upper body. Pose estimation is then run *only within this ROI*, saving significant computational resources.

3.  **Hand Detection**: The pose landmarks are used to pinpoint the location of the professor's wrist. A secondary, smaller ROI is created around the wrist to specifically search for hand gestures. This targeted approach ensures that only the professor's hand gestures are processed.

4.  **Re-acquiring Professor**: If the system can no longer see the professor's pose landmarks within the tracking ROI (e.g., if the professor walks off-camera), it reverts to the full-frame "RE-ACQUIRING" search mode until the professor is found again.