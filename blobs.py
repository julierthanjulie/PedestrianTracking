import numpy as np
import munkres

import pt_config

# Configuration constants.  Change these in pt_config
BLOB_LIFE = pt_config.BLOB_LIFE              # life of blob in frames, if not seen 
EDGE_THRESHOLD = pt_config.EDGE_THRESHOLD         # border of image, in pixels, which is regarded as out-of-frame
DISTANCE_THRESHOLD = pt_config.DISTANCE_THRESHOLD     # distance threshold, in pixels. If blob is further than this from previous position, update is ignored
MOVE_LIMIT = pt_config.MOVE_LIMIT          # maximum velocity of the blob. If outside this limit, velocity is disabled
MATCH_DISTANCE = pt_config.MATCH_DISTANCE         # maximum distance between blobs in the Hungarian algorithm matching step


blob_id = 0


class VirtualBlob:
	"""
	Represents a single pedestrian blob.
	"""

	def __init__(self, x,y):
		"""
		Create a new blob at the given (x,y) co-ordinate (in pixels). Each blob has a unique
		ID number, and a random color (for visulisation)
		"""

		global blob_id
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.life = BLOB_LIFE
		self.got_updated = False
		self.color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
		self.id = blob_id
		blob_id = blob_id + 1
	
	def update_location(self, x, y):
		"""Update the current state of the blob to the new given position, if it is 
		not too far away (<DISTANCE_THRESHOLD away) from the previous position"""
		if abs(x-self.x)<DISTANCE_THRESHOLD and abs(y-self.y)<DISTANCE_THRESHOLD:
			self.dx = 0.65*self.dx + 0.35*(x - self.x)
			self.dy = 0.65*self.dy + 0.35*(y - self.y)
			self.x = 0.6*self.x + 0.4*x
			self.y = 0.6*self.y + 0.4*y
			self.life = BLOB_LIFE
			self.got_updated = True

	def set_location(self, x, y):
		"""Change the position of the blob _without_ any distance filtering or velocity calculation."""
		self.x = x
		self.y = y
		
	def move(self):			
		"""Apply the current estimated velocity to the blob; used when the blob is not observed in the scene"""
		if abs(self.dx) < MOVE_LIMIT and abs(self.dy) < MOVE_LIMIT:
			self.x += self.dx
			self.y += self.dy
	
	def decay(self):
		"""Age the blob by one unit. When life<=0, return True, else return False"""
		# update location using velocity
		# die a bit
		self.life = self.life - 1
		return self.life<=0
		
	def __repr__(self):
		return "(%d, %d, %d, %d)" % (self.x, self.y, self.dx, self.dy)
		
		
		
class BlobTracker:
	"""The tracker object, which keeps track of a collection of pedestrian blobs"""
	def __init__(self):
		"""Initialise a new, empty tracker"""
		self.virtual_blobs = []
		self.traces = {}
		self.frame = 0
		self.is_inited=False
		
	def init_blobs(self, blobs, fnum):
		"""Initialise a set of blobs, from a list of initial (x,y) co-ordinates, in the format
		[(x,y), (x,y), ... ] """
		# initialise virtual blobs to be blobs 
		self.virtual_blobs = []
		for blob in blobs:
			v = VirtualBlob(blob[0], blob[1])
			self.virtual_blobs.append(v)
			self.traces[v.id] = [(v.x, v.y, fnum)]
		self.is_inited = True
		
	#returns true is this blob is within the frame
	def check_frame(self, blob, frame):
		"""Given an (x,y) co-ordinated, check if that position is inside the central frame (i.e. is 
		not inside the border region"""
		
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
		
				
	def track_blobs(self, blobs, frame, fnum):
		"""Main update call. Takes a list of new, observed blob co-ordinates, a rectangular frame specifier of the form 
		 [left, bottom, right, top] and a frame number, and updates the positions of the virtual blobs."""
		
		
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
		
		copy_distances = np.array(distance_matrix)
		
		m = munkres.Munkres()
		ot = m.compute(distance_matrix)
		rows = [t[1] for t in ot]
				
		# clear the update flag
		for v in self.virtual_blobs:
			v.got_updated = False
				
		# blobs on rows
		for i,matching_virtual in enumerate(rows):
			if i<len(blobs):
				blob = blobs[i]
				if matching_virtual<len(self.virtual_blobs):
					if copy_distances[i][matching_virtual]< MATCH_DISTANCE:
						self.virtual_blobs[matching_virtual].update_location(blob[0], blob[1])
					elif self.check_frame(blob, frame):
						
						v = VirtualBlob(blob[0], blob[1])
						self.virtual_blobs.append(v)
						self.traces[v.id] = [(v.x, v.y, fnum)]
				else:
					# new baby blobs!
					spawn = False
					# left
					if blob[0]<frame[0]+EDGE_THRESHOLD:
						spawn = True
					# right
					if blob[0]>frame[2]-EDGE_THRESHOLD:
						spawn = True
					# top
					if blob[1]<frame[1]+EDGE_THRESHOLD:
						spawn = True
					# bottom
					if blob[1]>frame[3]-EDGE_THRESHOLD:
						spawn = True
					
					if spawn:						
						v = VirtualBlob(blob[0], blob[1])
						self.virtual_blobs.append(v)
						self.traces[v.id] = [(v.x, v.y, fnum)]
					else:
						pass
						
				
		# deal with un-updated blobs
		graveyard = []
		for v in self.virtual_blobs:
			if not v.got_updated:
				# move, and reduce life counter
				if v.decay():
					#print "Virtual blob %s finally died." % v
					graveyard.append(v)
					
			# append trace of blob movement
			self.traces[v.id].append((v.x, v.y, fnum))
					
		# clean up the bodies
		for v in graveyard:
			self.virtual_blobs.remove(v)
