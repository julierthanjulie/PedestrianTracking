Quickstart for Pedestrian Tracking
==================================

The pedestrian tracker include a sample video that demonstrates the pedestrian tracker in action.  To see a demo of the pedestrian tracker, and test your local environment has all the required dependencies with::

	python pedestrian_tracking.py

.. figure::  images/demo.png
   :align:   center

   The sample video included in this project will run if your local environment is properly setup with all the dependencies.  The video preview will visualise pedestrian traffic as the processing is completed.

All resources are developed in `Python <https://www.python.org/>`_ (2.7).  Video preparation was completed using `ffmpeg <http://www.ffmpeg.org>`_ (mjpeg codec used, although any format supported by OpenCV is acceptable).


Please ensure the following dependencies are installed before using this tool:

* `OpenCV <http://opencv.org>`_

* <a href="http://www.numpy.org/">Numpy</a></li>

* <a href="http://wiki.scipy.org/PyLab">PyLab</a></li>

* <a href="http://www.scipy.org/">SciPy</a></li>

* <a href="https://pypi.python.org/pypi/hungarian/0.2.3">Hungarian Algorithm for Python</a>
