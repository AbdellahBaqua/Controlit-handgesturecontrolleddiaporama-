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

        python your_main_script_name.py


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
   * - **0** (e.g., Open Mouth)
     - Activates "Speech Mode" for 5 seconds.
   * - **1** (e.g., Five / Open Palm)
     - Presses :kbd:`F5` (Typically starts a slideshow).
   * - **2** (e.g., Fist)
     - Presses :kbd:`Spacebar` (Typically advances a slide).
   * - **3** (e.g., Pointing Left)
     - Presses the :kbd:`Left Arrow` key (Previous slide).


Voice Commands
--------------

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