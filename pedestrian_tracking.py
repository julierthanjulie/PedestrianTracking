"""  
This code is authored by Julie R. Williamson and John Williamson.
Julie.Williamson@glasgow.ac.uk, JohnH.Williamson@glasgow.ac.uk

If using this code or the associated materials, please cite this source.
The original publication is available at:
http://juliericowilliamson.com/blog/wp-content/uploads/2014/05/Williamson-small.pdf

Williamson, J.R. and Williamson, J.  Analysing Pedestrian Traffic Around Public Displays.  
In the Proceedings of Pervasive Displays 2014.  ACM, New York, USA.

"""

#  Please ensure the following dependencies are installed before use:
import cv2
import sys, getopt
import blobs
import numpy as np
import time

#  The frame is used to detect pedestrians entering the frame of view, and to remove noise.
#  Blobs detected within the frame are treated differently than those outside the frame.
FRAME_WIDTH = 30


#  Show a video preview during vision processing
draw_video = True

#  Outputs all traces from this script as a CSV file
def write_traces(traces, file_name):
	"""
	This function writes CSV data for each trace in the format PedestrianID , X, Y, FrameNumber;
	"""

	trace_f = open(file_name + "_traces.csv", "w")
	for id in traces:
		for set in traces[id]:
			thing = "" + str(id) + "," + str(set[0]) + "," + str(set[1]) + "," + str(set[2]) + ";\n"
			trace_f.write(thing)
	trace_f.close()


 
 
def show_video(argv):
	"""
	Main Function for all video processing.  Defaults for this file are adjusted here.
	"""
	tracker = blobs.BlobTracker()

	#  Testing MOG
	bgs_mog = cv2.BackgroundSubtractorMOG(500,10,0.9,2)
	

	video = "demo.avi"
	background = "/Users/julierwilliamson/Dropbox/ocv_python/alpha001.png"
	output =  "blob"
	method = "acc"
	
	file_name_base = ""
	
	try:
		opts,args = getopt.getopt(argv, "v:b:o:m:")
	except getopt.GetoptError:
		print "Getopt Error"
		exit(2)
	
	for opt, arg in opts:
		if opt == "-v":
			video = arg
		elif opt == "-b":
			background = arg
		elif opt == "-o":
			output = arg
		elif opt == "-m":
			method = arg
			
			
	
	print video , " " , background , " " , output
	
	file_name_base = "results/" + video.split("/")[-1].split(".")[-2]
		
	c = cv2.VideoCapture(video)
	
	#c.set(1, 26)
	_,f = c.read()
	#_,f = c.read()
	
	
	#cv2.imshow("back", f)
	
	if method == "ext":
		#  Use a predetermined background image
		c_zero = cv2.imread(background)
		#c_zero = f
	else:	
		#  Use the growing accumulated average		
		c_zero = np.float32(f)

	c.set(0, 000.0) 
	width = int(c.get(3))
	height = int(c.get(4))
	fps = int(c.get(5))
	fourcc = c.get(6)
	frames = c.get(7)
	
	print fourcc, fps, width, height, frames
	
	#writer = cv2.VideoWriter(output, 0,  fps, (width, height)) 
	
	# Celtic Connection Errosion/Dilation
	# for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
	# for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,40))

	# MOG Errosion/Dilation
	# for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	# for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,20))

	# Default Erosion.Dilation
	for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,10))	
	for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,20))


	orange = np.dstack(((np.zeros((height, width)),np.ones((height, width))*128,np.ones((height,width))*255)))
	ones = np.ones((height, width, 3))
	
	trails = np.zeros((height, width, 3)).astype(np.uint8)
	start_t = time.clock()	
	current_frame = 0
	while 1:
		
		#s = raw_input()
		
		_,f = c.read()
		current_frame = c.get(1)
		#print current_frame
		#print "Percentage: " , int((current_frame/frames)*100) , " Traces: " , len(tracker.traces)
		t = time.clock()-start_t
		remainder = 1.0 - current_frame/float(frames)
		current = current_frame/float(frames)
		remaining = int(((t/current)*remainder) / 60.0)
		
		if current_frame%20==0:
			print "Percentage: " , int((current_frame/frames)*100) , " Traces: " , len(tracker.traces), "Time left (m): ", remaining
		
		
		
		if method == "acc":
			cv2.accumulateWeighted(f, c_zero, 0.01)
			
		
		fgmask = bgs_mog.apply(f)

		
		#im_zero = cv2.convertScaleAbs(c_zero)
		im_zero = c_zero.astype(np.uint8)
	
		#  Get the first diff image - this is raw motion 
		d1 = cv2.absdiff(f, im_zero)
	
		#  Convert this to greyscale
		gray_image = cv2.cvtColor(d1, cv2.COLOR_BGR2GRAY)
		
		
		#  ksize aperture linear size, must be odd
		#gray_smooth = cv2.medianBlur(gray_image, 5)

		#  Turn this into a black and white image (white is movement)
		thresh, im_bw = cv2.threshold(gray_image, 15, 255, cv2.THRESH_BINARY)
		
		#bw_smooth = cv2.medianBlur(im_bw, 1)
		
		#im_bw_smooth = cv2.medianBlue(im_bw, (5,5), 0)
		
		cv2.imshow("MOG Subtracted", fgmask)
		#cv2.imshow("Image", f)
		#cv2.imshow("Background", im_zero)
		#cv2.imshow('Background Subtracted', d1)
		cv2.imshow("Thresholded", im_bw)
		
		
		
		# For using Motion Detection/Accumulated Image
		# im_er = cv2.erode(im_bw, for_er)
		# im_dl = cv2.dilate(im_er, for_di)

		# For using MOG algorithm background subtraction
		im_er = cv2.erode(im_bw, for_er)
		im_dl = cv2.dilate(im_er, for_di)

		contours, hierarchy = cv2.findContours(im_dl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
		my_blobs = []
		for cnt in contours:
			try:
				x,y,w,h = cv2.boundingRect(cnt)
				
				#print "Rect: " , w , " " , h
				cv2.rectangle(f, (x,y), (x+w, y+h), (255,0,0), 2)
				
				moments = cv2.moments(cnt)
				x = int(moments['m10'] / moments['m00'])
				y = int(moments['m01'] / moments['m00'])
				
				my_blobs.append((x,y))
			except:
				print "Bad Rect"

		#print len(my_blobs)
		
		if len(my_blobs) > 0:
			tracker.track_blobs(my_blobs, [0,0,width,height], current_frame)
		
			for v in tracker.virtual_blobs:
				cv2.rectangle(f, (int(v.x),int(v.y)), (int(v.x+5), int(v.y+5)), v.color, 2)
		
		#  Get blank image setup
		
		
			
		
		if draw_video:
			
			#total_trails = np.zeros((height,width,3), np.uint8)
			#alpha_trails = np.zeros((height,width,3), np.float64)
			#inv_alpha = np.zeros((height, width, 3), np.float64)
			
			for id in tracker.traces:
			
				ox = None
				oy = None
			
				#this_trail = np.zeros((height,width,3), np.uint8)
				#blank = np.zeros((height,width,3), np.uint8)
				#alpha = np.zeros((height, width, 3), np.uint8)

				if len(tracker.traces[id])>2:
					for pos in tracker.traces[id][-3:]:
				
						x = int(pos[0])
						y = int(pos[1])
				
						if ox and oy:
							sx = int(0.8*ox + 0.2*x)
							sy = int(0.8*oy + 0.2*y)
										
							#  Colours are BGRA					
							cv2.line(trails, (sx,sy), (ox, oy), (0,128,255), 1)
							#cv2.line(alpha, (sx, sy), (ox, oy), (255,255,255), 2)
					
							oy = sy
							ox = sx
						else:
							ox,oy = x,y
			
			
				#alpha_trails = alpha_trails + 0.001*alpha
		
			# f = (1-alpha)*f + alpha*orange
			#inv_alpha = cv2.subtract(ones, alpha_trails)
			#cv2.multiply(inv_alpha, f, f, 1, cv2.CV_8UC3)
			#alpha_trails = cv2.multiply(alpha_trails, orange, alpha_trails)
			#f = cv2.add(f, alpha_trails, f, None, cv2.CV_8UC3)  
		
			cv2.add(f,trails,f) 
			cv2.drawContours(f,contours,-1,(0,255,0),1) 
		
			#  draw frame
			cv2.rectangle(f, (FRAME_WIDTH,FRAME_WIDTH) ,(width-FRAME_WIDTH,height-FRAME_WIDTH), (0,0,0),2)
		
			#  Current output		
			cv2.imshow('output',f)
			cv2.waitKey(delay=1)
			
		
		
		if frames == current_frame:
			
			#  Save the pic
			cv2.imwrite(file_name_base + "_last_frame.png", f)
			
			write_traces(tracker.traces, file_name_base)

			
			#  Save tracker traces
			
			break
			
			
	
			#  Kill switch
		if current_frame%10==0 and draw_video:
			k = cv2.waitKey(1)
		else:
			k = 0
			
		if k == 27: # escape to close
			break
	
	

	cv2.destroyAllWindows()
	c.release()


if __name__ == "__main__":
	show_video(sys.argv[1:])