===========
Usage Guide
===========

This guide explains how to run the application and use its features.

Running the Application
-----------------------

1.  Open a terminal and navigate to your project's root directory.
2.  If you are using a virtual environment, make sure it is activated.
3.  Run the main Python script:

    .. code-block:: bash

        python app.py


System Workflow
---------------

The application operates using a simple state machine:

1.  **Authentication**: When the app starts, the camera window will open. The presenter must look at the camera. The system will search for their face and match it against the one in :file:`professor.jpg`.

2.  **Tracking**: Once the presenter is identified, the system switches to "TRACKING ACTIVE" mode. It will now follow the presenter's pose and look for hand gestures.

3.  **Control**: While tracking, the presenter can use hand gestures and voice commands to control their presentation.


Commands
========

The system responds to both hand gestures and voice commands.

Gesture Commands
----------------

These commands are always active when the system is in "TRACKING ACTIVE" mode.

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - Gesture (Trained ID)
     - Action
   * - **0** (e.g., Open Palm)
     - Activates "Speech Mode" for 5 seconds.
   * - **1** (e.g., Fist)
     - Presses :kbd:`F5` (Typically starts a slideshow).
   * - **2** (e.g., Peace Sign)
     - Presses :kbd:`Spacebar` (Stops the slideshow).
   * - **3** (e.g., Pointing Left)
     - Presses the :kbd:`Left Arrow` key (Previous slide).
   * - **4** (e.g., Pinch )
     - Presses the :kbd:`Right Arrow` key (Next slide).




Voice Commands
--------------
.. note::
  To complement the gesture-based system, the application incorporates a voice command module powered by the **Vosk** offline speech recognition toolkit. This feature is not perpetually active; it is deliberately enabled for a five-second window upon performing a specific hand gesture. Once activated, a lightweight Natural Language Processing (NLP) layer parses the incoming audio for key commands. This NLP model performs keyword spotting, trained to recognize core actions like ``next``, ``previous``, and ``quit``, along with their common aliases (e.g., ``back``, ``forward``, ``exit``). This gesture-to-speech activation mechanism serves as a robust filter, ensuring that vocal commands are only processed when explicitly intended by the presenter.
.. note::
   Voice commands are **only** active after you have used the "Activate Speech Mode" gesture (ID 0). The on-screen status text will turn green to confirm. You have 5 seconds to speak a command before the mode times out.

.. list-table::
   :widths: 40 40
   :header-rows: 1

   * - Spoken Keyword(s)
     - Action
   * - ``next``, ``forward``, ``right``
     - Presses the :kbd:`Right Arrow` key.
   * - ``previous``, ``backward``, ``back``, ``left``
     - Presses the :kbd:`Left Arrow` key.
   * - ``quit``, ``exit``, ``close``
     - Shuts down the application.


Additional Controls
-------------------

* **Toggle Debug View**: Press the :kbd:`d` key to toggle the visual overlay of landmarks and tracking boxes.
* **Force Quit**: Press :kbd:`q` or :kbd:`Esc` to immediately close the application.