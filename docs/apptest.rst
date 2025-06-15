.. gui_app.py documentation master file, created by Gemini.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

############################
Gesture Control GUI (`gui_app`)
############################

This module contains the main graphical user interface (GUI) for the Professor Gesture Control application. It provides the visual components and handles the user interaction for starting and stopping the computer vision backend.

The application window displays the camera feed and provides controls to manage the vision processing thread. It communicates with the backend through a queue system to ensure the GUI remains responsive.

.. contents::
   :local:

---

Module: `gui_app`
==================

.. automodule:: gui_app
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Description

   The main entry point for the application. This module sets up the CustomTkinter window, manages the layout of widgets (video feed, buttons, status bar), and handles the lifecycle of the computer vision background thread.

   .. autoclass:: gui_app.App(parent=None)
      :members:

      .. rubric:: Class Overview

      The main application class, inheriting from ``customtkinter.CTk``. It orchestrates the entire user interface and the interaction with the ``VisionBackend``.

      .. automethod:: __init__()

         Initializes the main application window, configures the appearance, and sets up all the necessary widgets and state variables, including the communication queue and threading events.

      .. automethod:: start_vision_thread()

         Handles the 'Start' button click. It initializes the ``VisionBackend`` and launches the main processing loop in a separate, non-blocking daemon thread. It also updates the GUI to reflect the running state.

      .. automethod:: stop_vision_thread()

         Handles the 'Stop' button click. It safely signals the vision thread to terminate using a ``threading.Event`` and updates the GUI to the 'stopped' state.

      .. automethod:: poll_queue()

         A recurring method that checks a ``queue.Queue`` for messages sent from the background vision thread. It updates the GUI with new video frames and status messages. This is the primary mechanism for thread-safe communication from the backend to the GUI.

      .. automethod:: on_closing()

         A handler for the window close event (clicking the 'X' button). It ensures the vision thread is stopped gracefully before the application exits.

.. rubric:: How to Run

To run the application, execute this script directly from your terminal:

.. code-block:: bash

   python gui_app.py
