======================
Hand Gesture Recognition(app.py) 
======================

Overview
--------

This application provides real-time hand gesture recognition using computer vision techniques. It tracks hand movements through a webcam and recognizes predefined hand gestures, which can trigger keyboard actions like pressing the spacebar or refreshing a page.

Dependencies
-----------

- Python 3.6+
- OpenCV
- MediaPipe
- PyTorch
- NumPy
- PyAutoGUI
- CSV

Installation
-----------

.. code-block:: bash

    pip install opencv-python mediapipe numpy torch pyautogui

Architecture
-----------

The application consists of several components:

1. **Main Module**: Handles the webcam feed and orchestrates the detection and classification process.
2. **Keypoint Classifier**: A PyTorch model that classifies hand postures based on landmark positions.
3. **Point History Classifier**: Classifies gestures based on movement patterns over time.
4. **Utilities**: Helper functions for calculating FPS and other operations.

Usage
-----

.. code-block:: bash

    python app.py [options]

Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 50

   * - Argument
     - Default
     - Description
   * - ``--device``
     - 0
     - Camera device index
   * - ``--width``
     - 960
     - Camera capture width
   * - ``--height``
     - 540
     - Camera capture height
   * - ``--use_static_image_mode``
     - False
     - Use static image mode instead of video
   * - ``--min_detection_confidence``
     - 0.7
     - Minimum confidence value for hand detection
   * - ``--min_tracking_confidence``
     - 0.5
     - Minimum confidence value for hand tracking

Controls
--------

- Press **ESC** to exit
- Press **0-9** to select a gesture label for recording
- Press **n** to switch to normal mode
- Press **k** to switch to keypoint recording mode
- Press **h** to switch to point history recording mode

Supported Gestures
-----------------

The application recognizes various hand gestures:

1. **Gesture 1**: Triggers F5 key (refresh)
2. **Gesture 3**: Triggers spacebar

A cooldown period of 2 seconds prevents repeated actions.

Technical Details
----------------

Hand Detection and Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~

The application uses MediaPipe's Hand solution to:

1. Detect hands in the camera feed
2. Track 21 hand landmarks (finger joints and palm points)
3. Identify whether the detected hand is left or right

Data Processing
~~~~~~~~~~~~~~

For each detected hand:

1. Calculate a bounding rectangle
2. Extract and normalize landmark coordinates
3. Preprocess the data for model input
4. Store point history for movement-based gestures

Classification
~~~~~~~~~~~~~

Two classification models are used:

1. **Keypoint Classifier**: Identifies static hand poses using landmark positions
2. **Point History Classifier**: Recognizes dynamic gestures based on fingertip movement patterns

Each model outputs a label that corresponds to a predefined gesture.

Data Collection
~~~~~~~~~~~~~

The application supports recording training data:

- In keypoint recording mode (mode 1), static hand poses are saved
- In point history mode (mode 2), fingertip movement patterns are recorded

Data is saved to CSV files for later model training.

Visualization
~~~~~~~~~~~~

The application provides real-time visual feedback:

1. Hand landmarks and connections
2. Bounding rectangle around the detected hand
3. Recognized gesture label
4. Mode and FPS information

File Structure
-------------

.. code-block:: none

    .
    ├── app.py                    # Main application
    ├── model/
    │   ├── keypoint_classifier/
    │   │   ├── keypoint_classifier_pyt.py    # PyTorch classifier model
    │   │   ├── keypoint_classifier_weights.pth  # Model weights
    │   │   └── keypoint_classifier_label.csv    # Label definitions
    │   └── point_history_classifier/
    │       ├── point_history_classifier.py      # Point history model
    │       └── point_history_classifier_label.csv  # Label definitions
    └── utils/
        └── cvfpscalc.py          # FPS calculation utility

Functions
--------

.. function:: main()

   Main function that initializes camera, loads models, and runs the detection loop.

.. function:: select_mode(key, mode)

   Handles key presses to switch between application modes.

   :param key: Key code from OpenCV waitKey
   :param mode: Current mode
   :return: (number, mode) tuple

.. function:: calc_bounding_rect(image, landmarks)

   Calculates the bounding rectangle around hand landmarks.

   :param image: Input image
   :param landmarks: MediaPipe hand landmarks
   :return: Rectangle coordinates [x1, y1, x2, y2]

.. function:: calc_landmark_list(image, landmarks)

   Converts MediaPipe landmarks to pixel coordinates.

   :param image: Input image
   :param landmarks: MediaPipe hand landmarks
   :return: List of landmark coordinates

.. function:: pre_process_landmark(landmark_list)

   Normalizes landmark coordinates for model input.

   :param landmark_list: List of landmark coordinates
   :return: Preprocessed landmark list

.. function:: pre_process_point_history(image, point_history)

   Preprocesses fingertip movement history.

   :param image: Input image
   :param point_history: Deque of fingertip positions
   :return: Preprocessed point history

.. function:: logging_csv(number, mode, landmark_list, point_history_list)

   Records data to CSV files for model training.

   :param number: Gesture label (0-9)
   :param mode: Current application mode
   :param landmark_list: Preprocessed landmark list
   :param point_history_list: Preprocessed point history

.. function:: draw_landmarks(image, landmark_point)

   Draws hand skeleton and landmarks on the image.

   :param image: Input image
   :param landmark_point: List of landmark coordinates
   :return: Image with landmarks

.. function:: draw_bounding_rect(use_brect, image, brect)

   Draws the bounding rectangle around the hand.

   :param use_brect: Flag to determine if rectangle should be drawn
   :param image: Input image
   :param brect: Rectangle coordinates
   :return: Image with bounding rectangle

.. function:: draw_info_text(image, brect, handedness, hand_sign_text, finger_gesture_text)

   Adds text information about detected hand and gesture.

   :param image: Input image
   :param brect: Rectangle coordinates
   :param handedness: Left/right hand information
   :param hand_sign_text: Recognized hand sign label
   :param finger_gesture_text: Recognized finger gesture label
   :return: Image with text information

.. function:: draw_point_history(image, point_history)

   Visualizes fingertip movement history.

   :param image: Input image
   :param point_history: Deque of fingertip positions
   :return: Image with point history visualization

.. function:: draw_info(image, fps, mode, number)

   Adds FPS, mode, and number information to the image.

   :param image: Input image
   :param fps: Current FPS value
   :param mode: Current application mode
   :param number: Selected gesture label
   :return: Image with information overlay

Model Training
-------------

To train custom gesture models:

1. Run the application in recording mode (k or h)
2. Press number keys (0-9) to assign gesture labels
3. Perform gestures to record training data
4. Use the collected CSV data to train the models

Extending the Application
------------------------

Adding New Gestures
~~~~~~~~~~~~~~~~~

1. Record data for new gestures using the recording modes
2. Retrain the models using the updated datasets
3. Update the label CSV files with new gesture names
4. Modify the code to handle new gesture IDs

Adding New Actions
~~~~~~~~~~~~~~~~

In the main detection loop, add new conditions to trigger different actions:

.. code-block:: python

    if hand_sign_id == NEW_GESTURE_ID:
        # Perform custom action
        pyautogui.press("YOUR_KEY")

Troubleshooting
--------------

- **No camera access**: Check device index with ``--device`` argument
- **Low FPS**: Reduce resolution with ``--width`` and ``--height``
- **Poor detection**: Ensure good lighting and adjust confidence thresholds
- **Gesture not recognized**: Try retraining with more varied examples

License
-------

[Controlit,2025]

Authors
-------

[Hachimboua, Baqua Abdellah]