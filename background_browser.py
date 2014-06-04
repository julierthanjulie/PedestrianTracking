import sys, getopt, cv2




def show_background(argv):
	
	video = "/Users/julierwilliamson/Dropbox/Pedestrian Traffic Installations/ShortTest2.mov"
	
	try:
		opts,args = getopt.getopt(argv, "v:")
	except getopt.GetoptError:
		print "Getopt Error"
		exit(2)
	
	for opt, arg in opts:
		if opt == "-v":
			video = arg
			
	c = cv2.VideoCapture(video)
	_,f = c.read()
	
	c.set(0, 000.0) 
	width = int(c.get(3))
	height = int(c.get(4))
	fps = int(c.get(5))
	fourcc = c.get(6)
	frames = c.get(7)
	
	#file_name_base = video.split("/")[-1].split(".")[-2]
	
	file_name_base = video[:-4]
	
	print file_name_base
	
	current_frame = 0
	
	while current_frame < frames:
		
		
		
		cv2.imshow("Background Selection", f)
		
		k = cv2.waitKey(0)
		
		print k
		
		if k == 115:
			print "Saving File"
			
			cv2.imwrite(file_name_base+ "_" + str(current_frame) + ".png", f)
			
		elif k == 63235:
			
			_,f = c.read()
			current_frame = c.get(1)
			
		elif k == 46:
			c.set(1, (current_frame+100))
			
			_,f = c.read()
			current_frame = c.get(1)
			
		elif k == 27:
			break
	
	





if __name__ == "__main__":
	show_background(sys.argv[1:])