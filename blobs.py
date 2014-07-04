import numpy as np
# import hungarian
import munkres

BLOB_LIFE = 25
EDGE_THRESHOLD = 20
DISTANCE_THRESHOLD = 50 
blob_id = 0

# Celtic Connections
# MOVE_LIMIT = 50

MOVE_LIMIT = 7

MATCH_DISTANCE = 50

class VirtualBlob:
	def __init__(self, x,y):
		global blob_id
		self.x = x
		self.y = y
		self.dx = 4
		self.dy = 4
		self.life = BLOB_LIFE
		self.got_updated = False
		self.color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
		self.id = blob_id
		blob_id = blob_id + 1
	
	def update_location(self, x, y):
		if abs(x-self.x)<DISTANCE_THRESHOLD and abs(y-self.y)<DISTANCE_THRESHOLD:
			
			self.dx = 0.8*self.dx + 0.2*(x - self.x)
			self.dy = 0.8*self.dy + 0.2*(y - self.y)
			self.x = 0.7*self.x + 0.3*x
			self.y = 0.7*self.y + 0.3*y
			self.got_updated = True
		
	def set_location(self, x, y):
		self.x = x
		self.y = y
		
	def move(self):			
		
		if abs(self.dx) < MOVE_LIMIT and abs(self.dy) < MOVE_LIMIT:
			#print "Moving: " , self.dx , " " , self.dy	
			self.x += self.dx
			self.y += self.dy
	
	def die_slightly(self):
		# update location using velocity
		# die a bit
		# return True if this blob is finally dead
		#d = np.sqrt(self.dx**2+self.dy**2)
		self.life = self.life - 1
		return self.life<=0
		
	def __repr__(self):
		return "(%d, %d, %d, %d)" % (self.x, self.y, self.dx, self.dy)
		
		
		
class BlobTracker:
	def __init__(self):
		self.virtual_blobs = []
		self.traces = {}
		self.frame = 0
		self.is_inited=False
		
	def init_blobs(self, blobs, fnum):
		# initialise virtual blobs to be blobs 
		self.virtual_blobs = []
		for blob in blobs:
			v = VirtualBlob(blob[0], blob[1])
			self.virtual_blobs.append(v)
			self.traces[v.id] = [(v.x, v.y, fnum)]
		self.is_inited = True
		#print "Creating initial blobs"
		#print self.virtual_blobs
	
	#returns true is this blob is within the frame
	def check_frame(self, blob, frame):
	
		#print "Blob: " , blob , " Frame: " , frame
		
		# Check Frame
		in_frame = False
		# left
		if blob[0]< frame[0]+EDGE_THRESHOLD:
			in_frame = True
		# right
		if blob[0]> frame[2]-EDGE_THRESHOLD:
			in_frame = True
		# top
		if blob[1]< frame[1]+EDGE_THRESHOLD:
			in_frame = True
		# bottom
		if blob[1]> frame[3]-EDGE_THRESHOLD:
			in_frame = True
		
		return in_frame	
		#return in_frame
	
				
	def track_blobs(self, blobs, frame, fnum):
		# frame will be [left, bottom, right, top]
		
		#print "Observed Blobs: " , len(blobs) , " Virtual Blobs: " , len(self.virtual_blobs)
		
		# initialise if not already done so
		if not self.is_inited:
			self.init_blobs(blobs, fnum)
			return
		
		# get max length of blob lists
		max_size = max(len(blobs), len(self.virtual_blobs))
		
		distance_matrix = np.zeros((max_size, max_size))
		
		for v in self.virtual_blobs:
			v.move()
		
		# compute distance matrix		
		for i in range(max_size):
			if i>=len(blobs):
				distance_matrix[i,:] = 0
				# no matching blob/virtual blob
			else:
				for j in range(max_size):
					if j>=len(self.virtual_blobs):
						distance_matrix[i,j] = 0
					else:
						dx = blobs[i][0]-self.virtual_blobs[j].x
						dy = blobs[i][1]-self.virtual_blobs[j].y
						distance_matrix[i,j] = np.sqrt(dx**2 + dy**2)
						
		
		# get assignments
		#rows, cols = hungarian.lap(distance_matrix)
		
		#print distance_matrix
		
		copy_distances = np.array(distance_matrix)
		
		m = munkres.Munkres()
		ot = m.compute(distance_matrix)
		rows = [t[1] for t in ot]
		
		#print "Hungarian: " , rows
		
		# clear the update flag
		for v in self.virtual_blobs:
			v.got_updated = False
		
		
		# blobs on rows
		for i,matching_virtual in enumerate(rows):
			#print "I: " , i , " Matching Virtual: " ,  matching_virtual , " Distance: " , copy_distances[i][matching_virtual]
			if i<len(blobs):
				blob = blobs[i]
				if matching_virtual<len(self.virtual_blobs):
					if copy_distances[i][matching_virtual]< MATCH_DISTANCE:
						self.virtual_blobs[matching_virtual].update_location(blob[0], blob[1])
					elif self.check_frame(blob, frame):
						#make a baby
						#print "Blob %d made a new blob baby!" % i
						
						v = VirtualBlob(blob[0], blob[1])
						self.virtual_blobs.append(v)
						#print v.x, v.y
						self.traces[v.id] = [(v.x, v.y, fnum)]
				else:
					# new baby blobs!
					make_baby = False
					# left
					if blob[0]<frame[0]+EDGE_THRESHOLD:
						make_baby = True
					# right
					if blob[0]>frame[2]-EDGE_THRESHOLD:
						make_baby = True
					# top
					if blob[1]<frame[1]+EDGE_THRESHOLD:
						make_baby = True
					# bottom
					if blob[1]>frame[3]-EDGE_THRESHOLD:
						make_baby = True
					
					if make_baby:
						#print "Blob %d made a new blob baby!" % i
						
						v = VirtualBlob(blob[0], blob[1])
						self.virtual_blobs.append(v)
						#print v.x, v.y
						self.traces[v.id] = [(v.x, v.y, fnum)]
					else:
						pass
						#print "Blob %d was a noise blob :("
				
		# deal with un-updated blobs
		graveyard = []
		for v in self.virtual_blobs:
			if not v.got_updated:
				# move, and reduce life counter
				if v.die_slightly():
					#print "Virtual blob %s finally died." % v
					graveyard.append(v)
					
			# append trace of blob movement
			self.traces[v.id].append((v.x, v.y, fnum))
					
		# clean up the bodies
		for v in graveyard:
			self.virtual_blobs.remove(v)
			