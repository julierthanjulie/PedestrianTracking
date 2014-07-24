Quickstart for Pedestrian Tracking
==================================

The pedestrian tracker includes a sample video that demonstrates the pedestrian tracker for three different detection modes.  If your environment has all the required dependencies, you should be able to run the following demonstration modes.

Basic Motion Detection
----------------------

This method used an accumulated image to generate an inferred background.  While this technique is more resilient to changes in lighting, objects that remain stationary are lost during tracking.  If no command line arguments are given, this is the default usage.::

	python pedestrian_tracking.py

Fixed Background Subtraction
----------------------------

This method requires a static background image and is not suitable for changing lighting conditions.  To use this method, you must provide a background image using -b in the command line arguments.  You can pull this directly from your video using the :doc:`background_browser`. :: 
	
	python pedestrian_tracking.py -m "ext" -b demo_0.png

Mixture of Gaussians Background Subtraction
-------------------------------------------

This method uses a more robust background inference technique and provides the best when Fixed Background Subtraction is not suitable.::
	
	python pedestrian_tracking.py -m "mog"

.. figure::  images/demo.png
   :align:   left

   The sample video included in this project will run if your local environment is properly setup with all the dependencies.  The video preview will give real time feedback about pedestrian traffic as the processing is completed.  This will show the raw output of the pedestrian tracker, which should then be validated before final visualisations are generated using :doc:`plot_trails`. 


Basic Usage
-----------

-v video				A video file to generate pedestrian trails. This code is optimised for MJPEG videos in an AVI container or MOV.

-b image				A background image (matching the size of the video) that must be provided if using Fixed Background Subtraction.

-m mode 				Set the background substraction mode.  Use acc for basic motion detection, ext for fixed background subtraction, and mog for mixture of gaussians background subtraction.

Results
---------

Upon completion, the python code will write all of the pedestrian traces to a CSV file.  The file will be named after the video and saved in the results folder.  The code will also generate a .log file describing the parameters used to generate the pedestrian trails and a .png file showing the raw output of the pedestrian trails.

Customisation
--------------

Once your development environment is fully setup and the demos can be run successfully, you are ready to run the pedestrian tracker on your own video.  Ensure your video is suitable for pedestrian tracking with our :doc:`videoguideline` and customise the tracking parameters for your video in :doc:`optimising`.


