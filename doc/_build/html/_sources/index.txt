.. Pedestrian Tracking documentation master file, created by
   sphinx-quickstart on Wed Jun  4 13:57:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pedestrian Tracking's documentation!
===============================================

Contents:

.. toctree::
   :maxdepth: 4

   quickstart
   videoguideline
   optimising
   visualisation
   overview



.. image::  images/BaselineTrails.png
   :align:   left

..

   These resources are available to analyse and visualise pedestrian traffic using computer vision. These files can generate behavioural maps and statistics about passers-by such as walking speed and direction. 

If using this code or the associated materials, please cite this source: 

Williamson, J.R. and Williamson, J. Analysing Pedestrian Traffic Around Public Displays. In the Proceedings of Pervasive Displays 2014. ACM, New York, USA.

The original publication is available at: `Performative Interaction Blog <http://juliericowilliamson.com/blog/wp-content/uploads/2014/05/Williamson-small.pdf>`_ and `The ACM Digital Library <http://dl.acm.org/citation.cfm?id=2611009.2611022&coll=DL&dl=ACM&CFID=517112652&CFTOKEN=16881151>`_. 

All the source code and data is available at: `GitHub <https://github.com/julierthanjulie/PedestrianTracking>`_, or download the `zip <https://github.com/julierthanjulie/PedestrianTracking/archive/master.zip>`_.

This documentation is a work in progress!  If you have specific questions, you can direct them to Julie.Williamson@glasgow.ac.uk.

Dependencies
--------------

All resources are developed in `Python <https://www.python.org/>`_ (2.7).  Video preparation was completed using `ffmpeg <http://www.ffmpeg.org>`_ (mjpeg codec used, although any format supported by OpenCV is acceptable).


Please ensure the following dependencies are installed before using this tool:

* `OpenCV <http://opencv.org>`_

* `Numpy <http://www.numpy.org/>`_

* `PyLab <http://wiki.scipy.org/PyLab>`_

* `SciPy <http://www.scipy.org/>`_

* `Munkres Hungarian Algorithm <https://pypi.python.org/pypi/munkres/>`_


Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

