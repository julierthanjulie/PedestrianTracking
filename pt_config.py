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
er_w = 7
er_h = 7

di_w = 15
di_h = 20

# #  Erosion and Dilation for MOG technique.  These are still under construction.
# mog_er_w = 12
# mog_er_h = 12

# mog_di_w = 20
# mog_di_h = 30

#  Erosion and Dilation for MOG technique.  These are still under construction.
mog_er_w = 7
mog_er_h = 7

mog_di_w = 16
mog_di_h = 26

#  Specify masks, for example a spherical display situated in the centre of the screen that should be masked out
#  masks = [(315,200,50,50)]

masks = []

"""
These parameters are used to configure blobs.py
"""
# Configuration constants
BLOB_LIFE = 15              # life of blob in frames, if not seen 
EDGE_THRESHOLD = 20         # border of image, in pixels, which is regarded as out-of-frame
DISTANCE_THRESHOLD = 60     # distance threshold, in pixels. If blob is further than this from previous position, update is ignored
MOVE_LIMIT = 15              # maximum velocity of the blob. If outside this limit, velocity is disabled
MATCH_DISTANCE = 20         # maximum distance between blobs in the Hungarian algorithm matching step



