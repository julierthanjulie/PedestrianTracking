#  This code generates frames from CSV values that can be stiched together using FFMPEG 
#  to animate pedestrian data.  This version produces an animation at 4x speed.

#  This code is authored by Julie R. Williamson and John Williamson.
#  Julie.Williamson@glasgow.ac.uk, JohnH.Williamson@glasgow.ac.uk

#  If using this code or the associated materials, please cite this source.
#  The original publication is available at:
#  http://juliericowilliamson.com/blog/wp-content/uploads/2014/05/Williamson-small.pdf

#  Williamson, J.R. and Williamson, J.  Analysing Pedestrian Traffic Around Public Displays.  
#  In the Proceedings of Pervasive Displays 2014.  ACM, New York, USA.

# The MIT License (MIT)

# Copyright (c) 2014 Julie R. Williamson and John Williamson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


print "Importing..."

#  Please ensure the following dependencies are installed before use:
import pylab
import numpy as np
import itertools
import sys, getopt
import operator
import collections


drawing_by_frame = []


#  
def generate_frames(argv):
	
	
	#  Some default values if nothing is provided in command line arguments.
	traces = 'bubble_pop_traces.csv'
	background = 'trails_480.png'
	
	#  Get command line arguments.
	#  -f specify a file name.  This code expects csv files in the format PedestrianID, X, Y, FrameNum
	#  -b specify a backgroun image.  Any format available to pylab is acceptable.	
	try:
		opts,args = getopt.getopt(argv, "f:b:")
	except getopt.GetoptError:
		print "Getopt Error"
		exit(2)
	
	for opt, arg in opts:
		if opt == "-f":
			traces = arg
		elif opt == "-b":
			background = arg

	#  Name each frame based on the filename		
	figure_name = traces.split("/")[-1].split(".")[-2]

	#  Load up csv file
	trace = np.loadtxt(traces, comments=';', delimiter=',')
	traces = itertools.groupby(trace, lambda x:x[0])
	
	#  These values should match those in pedestrian_tracking.py
	w,h=640,360
	border=20

	#  Some values from trail validation
	valid = 0
	avg_length = 0
	num_traces = 0

	#  Load up background image.
	background = pylab.imread(background)


	pylab.imshow(background)
	

	for id,t in traces:
		pts = np.array(list(t))
		invalid = False
	
		#  Validate Trails

		if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
			invalid = True

		if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
			invalid = True
		
		if len(pts) < 200:
			invalid = True
			
		if ((pts[0,2] > h-border) and (pts[0,1] > w/2-75 and pts[0,1] < w/2+75) or (pts[-1,2] > h-border) and (pts[-1,1] > w/2-75 and pts[-1,1] < w/2+75)):
			invalid = True

		
		#  For all valid trails, prepare them for generating animated trails by frame number	
		if not invalid:
					
			num_traces += 1
			avg_length += len(pts)
			
			#  Drawing colour for traces given as RGB
			colour = (0,0,1)
	
	
			for pt in pts:
				this_frame = [pt[3], pt[1], pt[2], pt[0]]				
				drawing_by_frame.append(this_frame)
					
			valid += 1
			
			x = np.clip(pts[:,1],0,w)
			y = np.clip(pts[:,2],0,h)
		
			
		
	print "Valid Trails: " , valid, " Average Length:" , avg_length/num_traces
	
	
	drawing_by_frame.sort()	
	
	last_frame = drawing_by_frame[-1][0]
	
	current_frame = drawing_by_frame[0][0]
	
	drawing_dict = collections.defaultdict(list)

	count = 0
	
	while len(drawing_by_frame) > 0:
	
		#print "Next Frame, " , current_frame
		pylab.imshow(background)
		
		while drawing_by_frame[0][0] == current_frame:
			list_one = drawing_by_frame.pop(0)
			
			x = drawing_dict[list_one[3]]
			x.append([list_one[1], list_one[2]])
			drawing_dict[list_one[3]] = x
			
		#  Adjust mod value here to adjust frame drawing frequency
		#  Draw stuff here
		if (current_frame % 10 ==0):
			print "Percentage Complete: " , (current_frame/last_frame)*100
			draw_dict(drawing_dict, w, h, border, figure_name, current_frame, count)

			count += 1
		
		pylab.clf()
		current_frame = drawing_by_frame[0][0]


def draw_dict(dict, w, h, border, figure_name, frame, count):
	for trace in dict:
		
		print trace
		pts = dict[trace]
	
		pylab.plot([p[0] for p in pts], [p[1] for p in pts],'-',color=(0,0,1),alpha=0.5, linewidth=2)	
		pylab.xlim(0,w)
		pylab.ylim(h,0)
		pylab.axis('off')
		pylab.subplots_adjust(0,0,1,1,0,0)
	pylab.savefig("Frames/" + figure_name + "_" + str(count).zfill(6) + '.png', dpi=150,bbox_inches='tight', pad_inches=0)	
	#pylab.savefig("Frames/" + 'frame' + str(int(frame)) + '.png', dpi=150,bbox_inches='tight', pad_inches=0)	
				

if __name__ == "__main__":

	print "Starting Frame Generation"
	generate_frames(sys.argv[1:])




