"""
These parameters are used to configure pedestrian_tracking.py
"""

#  The frame is used to detect pedestrians entering the frame of view, and to remove noise.
#  Blobs detected within the frame are treated differently than those outside the frame.

FRAME_WIDTH = 30

#  Show a video preview during vision processing.  Disabling this significantly reduced processing time.
#  A progress update will still be written out to the command line when this is updated.
draw_video = True

#  Errosion and Dilation rates to adjust accuracy of tracking/noise removal
er_w = 5
er_h = 10

di_w = 15
di_h = 20

#  Erosion and Dilation for MOG technique.  These are still under construction.
mog_er_w = 3
mog_er_h = 3

mog_di_w = 25
mog_di_h = 30

"""
These parameters are used to configure blobs.py
"""
# Configuration constants
BLOB_LIFE = 25              # life of blob in frames, if not seen 
EDGE_THRESHOLD = 20         # border of image, in pixels, which is regarded as out-of-frame
DISTANCE_THRESHOLD = 50     # distance threshold, in pixels. If blob is further than this from previous position, update is ignored
MOVE_LIMIT = 7              # maximum velocity of the blob. If outside this limit, velocity is disabled
MATCH_DISTANCE = 50         # maximum distance between blobs in the Hungarian algorithm matching step