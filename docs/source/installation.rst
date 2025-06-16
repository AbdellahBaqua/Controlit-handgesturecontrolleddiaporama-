======================
Installation and Setup
======================

Follow these steps to set up the project environment on your local machine.

Prerequisites
-------------

* Python 3.8 or newer.
* A webcam connected to your computer.
* A microphone connected and configured as the default input device.

Setup Steps
-----------

#. **Get the Code**

   It is assumed you have the project code in a directory on your computer.

#. **Create a Virtual Environment (Recommended)**

   Navigate to your project's root directory in your terminal and create a Python virtual environment.

   .. code-block:: bash

      # On macOS/Linux
      python3 -m venv venv
      source venv/bin/activate

      # On Windows
      python -m venv venv
      venv\Scripts\activate

#. **Install Python Dependencies**

   Install all required Python packages using pip.

   .. code-block:: bash

      pip install opencv-python mediapipe face_recognition pyautogui numpy torch sounddevice vosk

#. **Download the Vosk Speech Model**

   The system requires a speech model to function. Download the recommended small English model.

   1. Go to the `Vosk Models Page <https://alphacephei.com/vosk/models>`_.
   2. Download the model named **vosk-model-small-en-us-0.15**.
   3. Unzip the downloaded file.
   4. Move the resulting ``vosk-model-small-en-us-0.15`` folder into the root of your project directory.

#. **Set Up Project-Specific Files**

   The following files must be present in your project directory for the application to run:

   * **`professor.jpg`**: A clear photo of the presenter's face, located in the project root.
   * **`model/keypoint_classifier/`**: This directory must contain your trained gesture model (`keypoint_classifier_weights.pth`) and its labels (`keypoint_classifier_label.csv`).

Required File Structure
-----------------------

After setup, your project folder should look like this:

.. code-block:: text

    your-project-folder/
    │
    ├── your_main_script.py
    ├── professor.jpg
    │
    ├── vosk-model-small-en-us-0.15/
    │   ├── am/
    │   ├── conf/
    │   └── ... (other model files)
    │
    └── model/
        └── keypoint_classifier/
            ├── keypoint_classifier_weights.pth
            └── keypoint_classifier_label.csv

You are now ready to run the application.