=======================================
Gesture & Speech Presentation Control
=======================================

.. contents:: Table of Contents

Overview
========

This script enables a presenter to control a slideshow or application using a combination of real-time hand gestures and voice commands, captured through a standard webcam and microphone.

The system is designed to track a specific person (the "professor"), identify their hand gestures, and listen for voice commands to translate them into keyboard actions. This allows for a seamless, hands-free presentation experience.

The core workflow is a state machine:

#. **Search**: Initially, the system scans the camera feed to find a predefined person using face recognition.

#. **Track**: Once the person is found, it switches to a more efficient tracking mode. It uses pose estimation to follow the person's body and dynamically defines a Region of Interest (ROI) for hand detection.

#. **Listen & Act**: Within the tracking state, it actively looks for hand gestures and, when activated, listens for voice commands. Recognized commands are then executed as keyboard presses.


Core Features
=============

* **Face Recognition Lock-On**: The system only activates after identifying a specific individual from a :file:`professor.jpg` image file.

* **Pose-Based Tracking**: Uses ``MediaPipe Pose`` to efficiently track the presenter, ensuring the hand detection ROI is always correctly positioned.

* **Multi-Gesture Recognition**: Recognizes multiple distinct hand gestures (e.g., fist, open palm, pointing) using a custom-trained KeyPoint Classifier.

* **Voice Command Mode**: A specific hand gesture activates a voice recognition mode, allowing for commands like "next," "previous," and "quit."

* **Keyboard Emulation**: Uses ``pyautogui`` to simulate key presses, making it compatible with most presentation software (PowerPoint, Google Slides, etc.).

* **Debug Mode**: An optional visual overlay (the :kbd:`d` key to toggle) that shows the tracking boxes, pose landmarks, hand landmarks, and system status for easy troubleshooting.


Gesture & Speech Commands
=========================

The system responds to the following inputs. The "Speech Mode" must be activated with its gesture before any voice commands will be recognized.

.. list-table:: Command Reference
   :widths: 30 15 55
   :header-rows: 1

   * - Command (Input)
     - Type
     - Action
   * - ``Open Mouth / Specific Gesture``
     - Gesture
     - Activates "Speech Mode" for 5 seconds.
   * - ``Five / Open Palm``
     - Gesture
     - Presses :kbd:`F5` (Typically starts a slideshow).
   * - ``Fist``
     - Gesture
     - Presses :kbd:`Spacebar` (Typically advances a slide or plays media).
   * - ``Pointing Left``
     - Gesture
     - Presses the :kbd:`Left Arrow` key (Previous slide).
   * - ``"next"``, ``"right"``, ``"forward"``
     - Voice
     - Presses the :kbd:`Right Arrow` key (Next slide).
   * - ``"previous"``, ``"left"``, ``"back"``
     - Voice
     - Presses the :kbd:`Left Arrow` key (Previous slide).
   * - ``"quit"``, ``"exit"``, ``"close"``
     - Voice
     - Shuts down the application.