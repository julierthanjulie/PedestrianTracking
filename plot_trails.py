#  This code is authored by Julie R. Williamson and John Williamson.
#  Julie.Williamson@glasgow.ac.uk, JohnH.Williamson@glasgow.ac.uk

#  If using this code or the associated materials, please cite this source.
#  The original publication is available at:
#  http://juliericowilliamson.com/blog/wp-content/uploads/2014/05/Williamson-small.pdf

#  Williamson, J.R. and Williamson, J.  Analysing Pedestrian Traffic Around Public Displays.  
#  In the Proceedings of Pervasive Displays 2014.  ACM, New York, USA.

# The MIT License (MIT)

# Copyright (c) <year> <copyright holders>

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


#  Please ensure the following dependencies are installed before use:
import pylab
import numpy as np
import itertools
import sys, getopt
import scipy.signal, scipy.interpolate

w,h=640,360
border=20
table_x, table_y = 315, 200

def interactive_trails(traces):
	valid_trails = []

	for id,t in traces:
		pts = np.array(list(t))
		invalid = True
	
		# bad starting point
		if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
			invalid = True

		# bad ending point
		if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
			invalid = True

		# terminate around table		
		if (pts[-1,2] > h-border) and (pts[-1,1] > w/2-75 and pts[-1,1] < w/2+75):
			invalid = False
		
		fit = np.polyfit(pts[:,1], pts[:,2], 1)
		ys = np.polyval(fit, pts[:,1])
		rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		if rmse<2:
			invalid = True

		# too short
		if len(pts) < 250:
			invalid = True
		
		if not invalid:
			pts[:,1] = np.clip(pts[:,1],0,w)
			pts[:,2] = np.clip(pts[:,2],0,h)
			valid_trails.append(pts)
	return valid_trails

def min_validate_trails(traces):
	valid_trails = []

	for id,t in traces:
		pts = np.array(list(t))
		invalid = False

		# # bad starting point
		# if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
		# 	invalid = True

		# # bad ending point
		# if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
		# 	invalid = True
		
		# fit = np.polyfit(pts[:,1], pts[:,2], 1)
		# ys = np.polyval(fit, pts[:,1])
		# rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		# if rmse<2:
		#  	invalid = True


		# #  If line is straight, invalid
		# fit = np.polyfit(pts[:,1], pts[:,2], 1)
		# ys = np.polyval(fit, pts[:,1])
		# rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		
		# if rmse<2:
		# 	invalid = True
		# if rmse>=30:
		# 		invalid = True
	
		# too short
		# if len(pts) < 200:
		# 	invalid = True
	
		# total_distance = np.sqrt((pts[0,1]-pts[-1,1])**2+(pts[0,2]-pts[-1,2])**2)
		# if total_distance<300:
		#   		invalid = True

		if not invalid:
			pts[:,1] = np.clip(pts[:,1],0,w)
			pts[:,2] = np.clip(pts[:,2],0,h)
			valid_trails.append(pts)
	return valid_trails

def fake_validate(traces, straight):
	valid_trails = []

	for id,t in traces:
		pts = np.array(list(t))
		invalid = False


	
		# # bad starting point
		# if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
		# 	invalid = True

		# # bad ending point
		# if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
		# 	invalid = True

		# terminate around table		
		#if (pts[-1,2] > h-border) and (pts[-1,1] > w/2-75 and pts[-1,1] < w/2+75):
		#	invalid = False
		
		fit = np.polyfit(pts[:,1], pts[:,2], 1)
		ys = np.polyval(fit, pts[:,1])
		rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		if rmse<2:
			invalid = True

		if straight:
			if rmse>=30:
					invalid = True
		else:
			if rmse<30:
					invalid = True	
		# too short
		if len(pts) < 200:
			invalid = True
	
		total_distance = np.sqrt((pts[0,1]-pts[-1,1])**2+(pts[0,2]-pts[-1,2])**2)
		#print total_distance
		if total_distance<300:
				invalid = True

		if not invalid:
			pts[:,1] = np.clip(pts[:,1],0,w)
			pts[:,2] = np.clip(pts[:,2],0,h)
			valid_trails.append(pts)
	return valid_trails

def validate_trails(traces):
	valid_trails = []
	for id,t in traces:
		pts = np.array(list(t))
		invalid = False
	
		# bad starting point
		if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
			invalid = True

		# bad ending point
		if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
			invalid = True
		
		fit = np.polyfit(pts[:,1], pts[:,2], 1)
		ys = np.polyval(fit, pts[:,1])
		rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		if rmse<2:
			invalid = True

		# too short
		if len(pts) < 150:
			invalid = True
	
		# terminate around table		
		if ((pts[0,2] > h-border) and (pts[0,1] > w/2-75 and pts[0,1] < w/2+75) or (pts[-1,2] > h-border) and (pts[-1,1] > w/2-75 and pts[-1,1] < w/2+75)):
			invalid = True
	
		if not invalid:
			pts[:,1] = np.clip(pts[:,1],0,w)
			pts[:,2] = np.clip(pts[:,2],0,h)
			valid_trails.append(pts)
	return valid_trails


def test_trails(traces):
	valid_trails = []
	for id,t in traces:
		pts = np.array(list(t))
		invalid = False
	
		# bad starting point
		if (pts[0,1]>border and pts[0,1]<w-border) and (pts[0,2]>border and pts[0,2]<h-border):
			invalid = True

		# bad ending point
		if (pts[-1,1]>border and pts[-1,1]<w-border) and (pts[-1,2]>border and pts[-1,2]<h-border):
			invalid = False
		
		fit = np.polyfit(pts[:,1], pts[:,2], 1)
		ys = np.polyval(fit, pts[:,1])
		rmse = np.sqrt(np.mean((ys-pts[:,2])**2))
		if rmse<2:
			invalid = False

		# too short
		if len(pts) < 100:
			invalid = True
	
		# terminate around table		
		if ((pts[0,2] > h-border) and (pts[0,1] > w/2-75 and pts[0,1] < w/2+75) or (pts[-1,2] > h-border) and (pts[-1,1] > w/2-75 and pts[-1,1] < w/2+75)):
			invalid = False
	
		if not invalid:
			pts[:,1] = np.clip(pts[:,1],0,w)
			pts[:,2] = np.clip(pts[:,2],0,h)
			valid_trails.append(pts)
	return valid_trails

def get_velocity(trails):
	velocities = []
	smoothing = scipy.signal.get_window('hann', 30)
	smoothing = smoothing / np.sum(smoothing)

	for trail in trails:
		a,b = trail.shape
		p = np.zeros((a,b+4))
		p[:,0:4] = trail
		p[:,4] = np.gradient(trail[:,1])
		p[:,5] = np.gradient(trail[:,2])
		p[:,6] = np.sqrt(p[:,4]**2+p[:,5]**2)

		p[:,6] = scipy.signal.convolve(p[:,6], smoothing, mode='same')
		p[:,7] = np.arctan2(p[:,1], p[:,2])

		velocities.append(p)
	return velocities
			
def velocity_plot(csvfile):
	trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	traces = itertools.groupby(trace, lambda x:x[0])
	valid_trails = min_validate_trails(traces)
	valid_trails = get_velocity(valid_trails)
	trails = np.vstack(valid_trails)
	x,y = np.meshgrid(np.arange(0,w,20), np.arange(0,h,20))
	
	interp = scipy.interpolate.griddata((trails[:,1], trails[:,2]), trails[:,5]/trails[:,6], (x,y))
	pylab.imshow(interp, cmap='gist_heat', interpolation='nearest')
	pylab.show()


def draw_trails(trails, background=None, speed_range=None, y_range=None, colour=(0,0,1), spline=True, table_approach=False, draw_raw=False, line_width=2, draw_a=1):
	pylab.subplot(2,1,1)

	num_trails = 0

	if background!=None:
		pylab.imshow(background)
	for trail in trails:
		#pylab.plot(trail[:,1], trail[:,2], alpha=0.2, c='b')
		mean_speed = np.mean(trail[:,6])
		mean_y = np.mean(trail[:,2])

		
		use_trail = True
		if not(not speed_range or (speed_range[0]<mean_speed<speed_range[1])):
			use_trail = False
		if y_range and (mean_y<y_range[0] or mean_y>y_range[1]):
			use_trail = False

		if spline:
			x = trail[:,1]
			y = trail[:,2]
			t = np.arange(len(trail))
			spx = scipy.interpolate.UnivariateSpline(t,x,s=1e4,k=4)
			spy = scipy.interpolate.UnivariateSpline(t,y,s=1e4,k=4)
			spline_x = spx(t)
			spline_y = spy(t) 
		else:
			spline_x = trail[:,1]
			spline_y = trail[:,2]
			
		
		if use_trail:

			num_trails += 1
			end_distance = np.sqrt((trail[-1,1]-table_x)**2 + (trail[-1,2]-table_y)**2)
			alpha = np.clip(end_distance**-2*2000.0-0.05,0,1)
			
			if table_approach:
				#pylab.plot(x, y, alpha=alpha, c=(0,.3,1), lw=2)
				if alpha > .2:
					pylab.plot(spline_x, spline_y, alpha=alpha, c=colour, lw=line_width)
					print alpha
				
			else:
				pylab.plot(spline_x, spline_y, alpha=draw_a, c=colour, lw=line_width)
				if draw_raw:
					pylab.plot(x, y, alpha=draw_a, c=colour, lw=line_width)

			
	pylab.ylim(h-border,border)
	pylab.xlim(border,w-border)
	# if y_range:
	# 	pylab.axhline(y_range[0],c='g')
	# 	pylab.axhline(y_range[1],c='g')
		
	pylab.axis('off')
	pylab.subplot(2,1,2)
	speeds = [np.mean(trail[:,6]) for trail in trails]
	pylab.hist(speeds, bins=20)
	if speed_range:
		pylab.axvline(speed_range[0],c='r')
		pylab.axvline(speed_range[1],c='r')

	return num_trails



def plot_trails(csvfile, backgroundfile='trails_480.png'):

	background = pylab.imread(backgroundfile)

	# CC Data
	trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	traces = itertools.groupby(trace, lambda x:x[0])

	valid_trails = get_velocity(min_validate_trails(traces))

	# People Approaching the Display
	pylab.figure()
	all_trails = draw_trails(valid_trails, background=background, colour=(1, 0, 0), table_approach=True)

	# All Trails
	pylab.figure()
	all_trails = draw_trails(valid_trails, background=background, colour=(1, 1, 0), line_width=2, draw_a=.2)

	print all_trails

	# # Figure 1:  Chance Participants
	# trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	# traces = itertools.groupby(trace, lambda x:x[0])
	# vtraces = get_velocity(fake_validate(traces, straight=True))

	# pylab.figure()
	# draw_trails(vtraces, background=background, colour=(1,0,0), table_approach=True)
	
	# #  Figure 2:  Active Participants
	# trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	# traces = itertools.groupby(trace, lambda x:x[0])
	# ctraces = get_velocity(fake_validate(traces, straight=False))
	
	# pylab.figure()
	# draw_trails(ctraces, background=background, colour=(1,0,1), table_approach=True)

	# #  All Non-Interacting Users
	# trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	# traces = itertools.groupby(trace, lambda x:x[0])	
	# valid_trails = get_velocity(validate_trails(traces))

	# pylab.figure()
	# draw_trails(valid_trails, background=background, colour=(0, .8, 1))


	# #  VALIDATION
	# trace = np.loadtxt(csvfile, comments=';', delimiter=',')
	# traces = itertools.groupby(trace, lambda x:x[0])	
	# valid_trails = get_velocity(min_validate_trails(traces))

	# #  
	# pylab.figure()
	# all_trails = draw_trails(valid_trails, background=background, colour=(1, 0, 0))

	

	# #  Interested Avoiders 
	# pylab.figure()
	# interested = draw_trails(valid_trails, background=background, speed_range=[0, 2.2], y_range=[90,230], colour=(0,1,0))
	
	# #  Disinterested Avoiders
	# pylab.figure()
	# disinterested = draw_trails(valid_trails, background=background, speed_range=[2.5, 3.2], y_range=[0,170], colour=(0,1,1))
	
	# #  Disinterested Avoiders
	# pylab.figure()
	# busker = draw_trails(valid_trails, background=background, y_range=[0,120], colour=(1,1,1))


	# #  Assertive Avoiders
	# pylab.figure()
	# assertive = draw_trails(valid_trails, background=background, speed_range=[2.5, 3.2], y_range=[230,400], colour=(1,.5,0))

	# #  All within the table Avoiders
	# pylab.figure()
	# close_by = draw_trails(valid_trails, background=background, y_range=[230,400], colour=(1,1,0))


	# print "Chance passerby" , len(vtraces)
	# print "Active passerby" , len(ctraces)
	# print "Valid Trails" , len(valid_trails)
	# print "Red Trails", all_trails
	# print "Green Trails" , interested
	# print "Disinterested" , disinterested
	# print "Busker" , busker
	# print "Assertive" , assertive 

	# ys = []
	# for trail in valid_trails:
	# 	ys.append(np.mean(trail[:,2]))


	# print "Average Y for Non-Interacting", np.mean(ys)
	# print "Number Of Trails within Table", close_by
	
	pylab.show()

if __name__=="__main__":

	background = '/Users/julierwilliamson/Dropbox/ocv_python/Datas/trails_480.png'
	traces = '/Users/julierwilliamson/Dropbox/ocv_python/Extras/test_traces.csv'

	try:
		opts,args = getopt.getopt(sys.argv[1:], "f:b:")
	except getopt.GetoptError:
		print "Getopt Error"
		exit(2)

	for opt, arg in opts:
		if opt == "-f":
			traces = arg
		elif opt == "-b":
			background = arg

	#background = '/Users/julierwilliamson/Movies/Pedestrian Data/September 6 Dr Duck/dr_duck_background.png'
	#traces = '/Users/julierwilliamson/Movies/Pedestrian Data/Validation/validation_4_traces_ext.csv'

	# background = '/Users/julierwilliamson/Movies/Pedestrian Data/September 10 Bubble Pop/bubble_pop_background.png'
	# traces = '/Users/julierwilliamson/Movies/Pedestrian Data/September 10 Bubble Pop/bubble_pop_traces.csv'

	# background = '/Users/julierwilliamson/Movies/Pedestrian Data/September 9 Lost In Waves/lost_in_waves_background.png'
	# traces = '/Users/julierwilliamson/Movies/Pedestrian Data/September 9 Lost In Waves/lost_in_waves_traces.csv'

	# background = '/Users/julierwilliamson/Movies/Pedestrian Data/September 5 Busking/busker_background.png'
	# traces = '/Users/julierwilliamson/Movies/Pedestrian Data/September 5 Busking/busker_traces.csv'

	#background = '/Users/julierwilliamson/Movies/Pedestrian Data/August 9 Baseline/baseline_background.png'
	#traces = '/Users/julierwilliamson/Movies/Pedestrian Data/August 9 Baseline/traces_baseline_aug_9.csv'

	# background = '/Users/julierwilliamson/Movies/Pedestrian Data/August 22 LEDS_noninteractive/rainbow_chase_background.png'	
	# traces = '/Users/julierwilliamson/Movies/Pedestrian Data/August 22 LEDS_noninteractive/rainbow_chase_traces.csv'

	print "Background: ",  background
	print "Traces:" , traces
	plot_trails(traces, background)
	#velocity_plot(traces)

