=============================
Gesture Control GUI (guiapp.py)
=============================

Overview
--------

This application provides a user-friendly Graphical User Interface (GUI) for the real-time hand gesture recognition system. It serves as a visual wrapper around the core vision backend, displaying the live camera feed and allowing the user to easily start and stop the gesture detection process with the click of a button.

The GUI is built with CustomTkinter to ensure a modern look and feel. It is designed to be responsive and non-blocking by running the intensive computer vision tasks in a separate background thread.

Dependencies
-----------

- Python 3.6+
- OpenCV
- MediaPipe
- PyTorch
- NumPy
- CustomTkinter
- Pillow (PIL)
- PyAutoGUI

Installation
-----------

.. code-block:: bash

    pip install opencv-python mediapipe numpy torch customtkinter pillow pyautogui

Architecture
-----------

The GUI application's architecture is designed to keep the user interface responsive while handling heavy processing:

1.  **GUI Main Thread (App Class)**: Manages the CustomTkinter window, all widgets (buttons, video label), and user interactions. It does not perform any heavy computation.
2.  **Vision Backend Thread (VisionBackend Class)**: Runs the entire computer vision pipeline (camera capture, face detection, hand tracking, gesture classification) in a separate thread. This prevents the GUI from freezing.
3.  **Communication Queue**: A thread-safe queue (`queue.Queue`) is used to pass data (video frames, status messages) from the vision backend thread to the GUI thread for display.

Usage
-----

.. code-block:: bash

    python guiapp.py

After running the command, a GUI window will appear. Use the on-screen buttons to control the application.

Controls
--------

- **Start Button**: Begins the camera feed and activates the hand gesture recognition system.
- **Stop Button**: Halts the camera feed and stops the gesture recognition.
- **Window Close ('X') Button**: Safely stops the backend thread and closes the application.

Supported Gestures
-----------------

The backend recognizes the same gestures as the command-line application:

1.  **Gesture 1**: Triggers F5 key (refresh)
2.  **Gesture 3**: Triggers spacebar

A cooldown period of 2 seconds prevents repeated actions.

Technical Details
----------------

Hand Detection and Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~

The GUI relies on the same backend `VisionBackend` class, which uses MediaPipe's Hand solution to detect and track 21 hand landmarks in the camera feed.

GUI and Thread-Safe Communication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To prevent the GUI from becoming unresponsive, the application uses a multi-threaded approach:

1.  When the **Start** button is pressed, a new daemon thread is created for the `VisionBackend`.
2.  The `VisionBackend` captures video frames, processes them, and puts the resulting image (with overlays) into a shared `queue.Queue`.
3.  The GUI thread periodically polls this queue (using `poll_queue()`) to retrieve new frames and display them, ensuring smooth video playback without freezing.
4.  A `threading.Event` is used to signal the backend thread to stop gracefully when the **Stop** button is pressed or the window is closed.

Key Components
--------------

- **`App` Class**: The main CustomTkinter class. It builds the GUI layout, handles button clicks (`start_vision_thread`, `stop_vision_thread`), and manages the polling loop (`poll_queue`) to update the video feed from the queue.
- **`VisionBackend` Class**: The engine of the application. It contains all the OpenCV and MediaPipe logic. It runs in its own thread and communicates back to the `App` class via the shared queue.

Extending the Application
------------------------

Adding New GUI Elements
~~~~~~~~~~~~~~~~~~~~~

You can add new widgets like status labels or configuration options within the `App` class `__init__` method.

Displaying More Information
~~~~~~~~~~~~~~~~~~~~~~~~~

To display more information from the backend (e.g., the currently detected gesture), modify the `VisionBackend` to put new message types into the queue. Then, update the `poll_queue` method in the `App` class to handle these new messages and update the corresponding GUI elements.

Troubleshooting
--------------

- **GUI is frozen or unresponsive**: This could indicate that a long-running task is accidentally being run on the main GUI thread. Ensure all heavy processing is inside the `VisionBackend` thread.
- **Camera feed does not appear**: Verify that your webcam is connected and that the correct device index is being used within the `VisionBackend` class. Check the terminal for any OpenCV errors.
- **Application does not close properly**: Ensure the `on_closing` method correctly signals the `threading.Event` to stop the backend thread before shutting down.

License
-------

[Controlit,2025]

Authors
-------

[Hachimboua, Baqua Abdellah]