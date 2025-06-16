======================================================
Professor Gesture & Speech Control App
======================================================


External Files & Models
============================

The application relies on several external files that must be placed in the correct directory structure:

* ``professor.jpg``: An image file containing a clear picture of the "professor's" face. This must be in the same directory as the script.
* ``vosk-model-small-en-us-0.15/``: The Vosk speech recognition model directory. This must be in the same directory as the script.
* ``model/keypoint_classifier/keypoint_classifier_weights.pth``: The pre-trained PyTorch model weights for the hand gesture classifier.
* ``model/keypoint_classifier/keypoint_classifier_label.csv``: A CSV file containing the labels corresponding to the gesture classifier's output indices.
* ``model/keypoint_classifier/keypoint.csv``: A CSV file used for logging new hand gesture data.


 Command-line Arguments
===========================

The script accepts several optional command-line arguments:

.. option:: --device <int>

   Specifies the camera device ID. Default is ``0``.

.. option:: --width <int>

   Sets the capture width of the camera. Default is ``960``.

.. option:: --height <int>

   Sets the capture height of the camera. Default is ``540``.

.. option:: --use_static_image_mode

   A flag to indicate that MediaPipe should treat the video feed as a series of unrelated images.

.. option:: --min_detection_confidence <float>

   Sets the minimum confidence value (from 0.0 to 1.0) for the hand detection to be considered successful. Default is ``0.7``.

.. option:: --min_tracking_confidence <float>

   Sets the minimum confidence value (from 0.0 to 1.0) for the hand landmarks to be considered tracked successfully. Default is ``0.5``.

********************************
Architecture & Program Flow
********************************

The application operates as a state machine, managed by the ``current_mode`` variable within the main loop.

State 1: `SEARCHING_PROFESSOR_INITIAL`
===========================================

* This is the initial state upon startup.
* The system captures frames and resizes them by 50% for faster processing.
* It uses the `face_recognition` library to detect all faces in the down-scaled frame.
* For each detected face, it compares its encoding to the pre-loaded encoding from `professor.jpg`.
* If a match is found (with a tolerance of 0.55), the application stores the face's bounding box, prints "Professor Found!", and transitions to the `TRACKING_PROFESSOR` state.

State 2: `TRACKING_PROFESSOR`
==================================

This is the primary operational state where gesture and speech recognition occur.

1.  **Pose ROI Calculation**: It defines a large Region of Interest (ROI) around the professor's last known face position. This dramatically reduces the processing load as pose detection is only run on this smaller section of the image.
2.  **Pose Estimation**: MediaPipe Pose is run on the ROI.
3.  **Tracking & Face Box Update**:
    * If a pose is successfully detected, the system uses the stable positions of the nose and eye landmarks from the *pose* model to update the face bounding box. This is more robust than re-running face detection.
    * If the pose is lost (e.g., the professor walks off-screen), the system transitions to the `REACQUIRING_PROFESSOR` state.
4.  **Hand ROI Calculation**: It checks the visibility of the left wrist landmark from the pose model. If visible, it creates a *new, smaller, dynamic ROI* centered on the wrist's position.
5.  **Hand Landmark Detection**: MediaPipe Hands is run on this hand-specific ROI.
6.  **Gesture Classification**:
    * If a hand is detected, its 21 landmarks are extracted.
    * The landmarks are pre-processed (normalized relative to the wrist) and fed into the `KeyPointClassifier`.
    * The classifier returns a sign ID (e.g., 0 for 'Open', 1 for 'Start', etc.).
7.  **Action Execution**: Based on the gesture ID, and subject to a `1.5 second` cooldown, a `pyautogui` action is triggered.

State 3: `REACQUIRING_PROFESSOR`
=====================================

* This state is entered if pose tracking is lost.
* The logic is identical to the initial search state, but it displays a "RE-ACQUIRING" message.
* Once the professor is found again, it returns to the `TRACKING_PROFESSOR` state.

Speech Recognition Sub-System
==================================

* Speech recognition is controlled by the `is_speech_mode_active` boolean flag.
* This flag is set to `True` by a specific hand gesture (ID 0, "Open").
* When active, the system reads audio chunks from the microphone in a non-blocking manner within the main video loop.
* The audio is fed to the `Vosk` recognizer. When a complete phrase is recognized, the result is passed to `execute_speech_action`.
* `get_keyword` searches the recognized text for keywords ("next", "previous", "quit") and their aliases.
* If a keyword is found, a `pyautogui` action is triggered, subject to its own `1.5 second` cooldown.
* Speech mode automatically deactivates after 5 seconds of no new speech-activating gestures to prevent accidental command execution.

******************************
Module & Function Reference
******************************

This section details the key functions within the script.

Speech Recognition
=======================

.. function:: get_keyword(text: str) -> Optional[str]

   Parses a string to find pre-defined command keywords or their aliases.

   :param text: The input string from the speech recognizer.
   :returns: A canonical keyword ('next', 'previous', 'quit') or ``None`` if no keyword is found.

.. function:: execute_speech_action(recognized_text: str)

   Executes a keyboard command based on recognized speech. Enforces a 1.5-second cooldown between actions.

   :param recognized_text: The text output from the Vosk recognizer.
   :global is_speech_mode_active: Only runs if this is ``True``.

Image Processing & Landmark Calculation
============================================

.. function:: calc_bounding_rect(image, landmarks) -> list

   Calculates the bounding box coordinates for a set of MediaPipe landmarks.

   :param image: The source image.
   :param landmarks: The MediaPipe landmarks object.
   :returns: A list of four integers: ``[x_min, y_min, x_max, y_max]``.

.. function:: calc_landmark_list(image, landmarks) -> list

   Converts MediaPipe landmark objects into a list of pixel coordinates.

   :param image: The source image.
   :param landmarks: The MediaPipe landmarks object.
   :returns: A list of ``[x, y]`` coordinate pairs.

.. function:: pre_process_landmark(landmark_list) -> list

   Normalizes a list of landmark coordinates for the gesture classifier. It makes the landmarks relative to the first point (the wrist) and scales them by the maximum absolute value.

   :param landmark_list: A list of landmark coordinates from ``calc_landmark_list``.
   :returns: A flattened list of normalized floating-point values.

Data Logging & Debug Drawing
=================================

.. function:: logging_csv(number, mode, landmark_list, point_history_list)

   Saves the processed landmark list to a CSV file for training the gesture classifier. This is active only when ``mode`` is 1 (Logging Key Point).

   :param number: The class label (0-9) for the gesture being logged.
   :param mode: The current application mode.
   :param landmark_list: The normalized landmark list to be saved.

.. function:: draw_landmarks(image, landmark_point) -> image

   Draws stylized landmarks and connections on the image.

.. function:: draw_info_text(image, brect, handedness, hand_sign_text, finger_gesture_text) -> image

   Draws the recognized hand sign label above the hand's bounding box.

.. function:: draw_info(image, fps, mode, number) -> image

   Draws general application status information (FPS, Mode) on the screen.

Main Application
=====================

.. function:: main()

   The main entry point of the application. It handles initialization of all components (camera, models, etc.), contains the main application loop, manages state transitions, and orchestrates calls to all other processing and drawing functions.

****************************
Modes & Command Reference
****************************

In-App Controls
====================

* **'q' or 'ESC' Key**: Quit the application.
* **'d' Key**: Toggle Debug Mode. This shows/hides the pose/hand ROIs, landmarks, and other visual aids.
* **'k' Key**: Switch to "Logging Key Point" mode.
* **'n' Key**: Switch back to "Normal" mode.
* **'0'-'9' Keys**: When in Logging mode, logs the current hand gesture under the pressed number as a label.

Gesture & Voice Commands
=============================

The following table lists the recognized gestures and voice commands and their corresponding actions.

+---------------+--------------------+--------------------------------+----------------------------+
| Control Type  | Input              | Recognized Label (from .csv)   | Action                     |
+===============+====================+================================+============================+
| Gesture       | Open Palm          | 0: Open                        | Activate Speech Mode       |
+---------------+--------------------+--------------------------------+----------------------------+
| Gesture       | Pointing (Index)   | 1: Point / Start               | Press `F5` (Start Slideshow) |
+---------------+--------------------+--------------------------------+----------------------------+
| Gesture       | "OK" Sign          | 2: OK / Play/Pause             | Press `Spacebar`           |
+---------------+--------------------+--------------------------------+----------------------------+
| Gesture       | Thumb Left         | 3: Left / Previous             | Press `Left Arrow`         |
+---------------+--------------------+--------------------------------+----------------------------+
| Gesture       | Fist               | 4: Close / Quit                | Press `ESC` (End Slideshow)|
+---------------+--------------------+--------------------------------+----------------------------+
| Voice         | "next", "forward"  | -                              | Press `Right Arrow`        |
+---------------+--------------------+--------------------------------+----------------------------+
| Voice         | "previous", "back" | -                              | Press `Left Arrow`         |
+---------------+--------------------+--------------------------------+----------------------------+
| Voice         | "quit", "exit"     | -                              | Press `ESC`                |
+---------------+--------------------+--------------------------------+----------------------------+