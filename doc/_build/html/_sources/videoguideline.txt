Guidelines for Pedestrian Tracking Video
===========================================
This pedestrian tracking software builds on a few assumptions about the video frame a view in order to work properly. Ensure your video complies to these assumptions in order to ensure the best possible tracking.

Vantage Point
-------------

This software will work best on video that is taken from above.  For example, the sample videos from this distribution are filmed at 3 stories above ground level.  This height minimises the visual overlap between pedestrians and enables higher accuracy tracking.  Ideal video would be taken from a central point directly above the pedestrian traffic to be analysed.

Entrances and Exits
-------------------

The current version of this sofware assumes pedestrians will enter and exit within the edge of the video frame.  So, if you video includes a staircase in the centre of the frame, pedestrians entering from this location won't be tracked.

Video Format
------------

This software has been tested with ffmpeg encoded videos in avi and mov containers.  However, any supported OpenCV videos will still work with this software, but performance may be very slow for other video encodings.

ffmpeg
------

All the videos tested with this software have been manipulated using `ffmpeg <https://www.ffmpeg.org/>`_.