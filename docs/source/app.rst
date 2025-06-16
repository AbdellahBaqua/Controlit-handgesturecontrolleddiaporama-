========================
Application Architecture
========================

This document provides a technical overview of the main application script, its architecture, and its core components.

.. contents:: Table of Contents
   :local:
   :depth: 2

Architectural Overview
----------------------

The application is built using a **single-threaded architecture**. This design was deliberately chosen to resolve resource conflicts between the CPU-intensive video processing (for gesture recognition) and the real-time audio stream processing (for speech recognition).

By running all tasks within a single main loop, we prevent thread starvation and ensure that both gesture and speech inputs are handled responsively, even at the cost of a minor reduction in maximum potential framerate.

All application states are managed through a set of global variables.

Core Components
===============

Global State Management
-----------------------

The application's state is controlled by a few key global variables:

* ``app_is_running``: A boolean flag that controls the main `while` loop. When set to `False` (by the ``shutdown_app()`` function), the application will cleanly exit.
* ``is_speech_mode_active``: A boolean flag that determines if the system should process spoken words into commands. This is the primary "gatekeeper" for voice control.
* ``last_speech_gesture_time``: A timestamp recording when the speech activation gesture was last seen. Used to automatically time out and deactivate speech mode after 5 seconds of inactivity.
* ``last_speech_action_time``: A timestamp recording when the last successful voice command was executed. Used to enforce a cooldown period between voice commands.

The ``main()`` Function
--------------------

The ``main()`` function is the heart of the application and orchestrates all operations. Its workflow is divided into three main phases:

1.  **Initialization**
    
    * Loads the ``Vosk`` speech recognition model.
    * Parses command-line arguments.
    * Initializes the camera capture with ``OpenCV``.
    * Loads the ``face_recognition`` data from :file:`professor.jpg`.
    * Initializes ``MediaPipe`` models for pose and hand tracking.
    * Loads the custom gesture ``KeyPointClassifier`` model.

2.  **The Main Loop**
    
    * The primary `while app_is_running:` loop is wrapped within a ``sounddevice`` input stream context manager, ensuring the microphone is active.
    * Inside the loop, the following occurs on every iteration:

      * Keyboard input is checked for manual exit (:kbd:`q`) or debug mode toggling (:kbd:`d`).
      * The speech mode timeout is checked and updated.
      * A frame is read from the webcam.
      * If ``is_speech_mode_active`` is true, a chunk of audio is read from the microphone stream and passed to the Vosk recognizer.
      * The gesture recognition state machine is executed (searching for the professor, then tracking hands).
      * The final image with debug overlays is displayed.
      * A tiny ``time.sleep(0.001)`` is called to ensure the loop is "polite" and yields CPU time, which aids stability.

3.  **Cleanup**
    
    * After the loop exits, `cap.release()` and `cv.destroyAllWindows()` are called to free up system resources cleanly.

Speech Handling Functions
-------------------------

These are standalone functions that manage voice command logic:

* ``get_keyword(text)``: Takes the raw text recognized by Vosk and checks it against a dictionary of primary keywords (e.g., "next") and aliases (e.g., "forward"). It returns the standardized command if a match is found.

* ``execute_speech_action(text)``: This function acts as the final "gatekeeper." It receives recognized text, but first checks if ``is_speech_mode_active`` is `True`. If it is, it finds the keyword, checks the command cooldown, and only then executes the corresponding ``pyautogui`` action.

Gesture Utility Functions
-------------------------

The script contains numerous helper functions for processing video and gesture data.

* **``calc_*`` functions**: A group of functions like ``calc_bounding_rect()`` and ``calc_landmark_list()`` that perform mathematical calculations to process landmark data from MediaPipe into a usable format. ``pre_process_landmark()`` normalizes this data for the classifier.
* **``draw_*`` functions**: A group of functions like ``draw_landmarks()`` and ``draw_info()`` that use OpenCV to draw visual feedback (landmarks, bounding boxes, status text) onto the camera frame for debug mode.