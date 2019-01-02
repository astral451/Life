

class Data():
	'''
	The Data holds the grid and one Life object.  This is used for creation
	plus outside UI can see the object in this way.	
	'''

	def __init__( self, div ):
		self.grid = Grid( div )
		self.life = Life


	def create_life( self, x, y ):
		'''
		Creates a Life object at the given coordinates.  This
		internally formats the grid to the list.	

		:param x: The X coord in the grid
		:type x: int
		:param y: The Y coord in the grid
		:type y: int
		'''
		pos = self.grid_to_pos( x, y )
		life = self.life()
		self.grid.add_life( pos, life )


	def grid_to_pos( self, x, y ):
		'''
		Take a grid position in X,Y and convert to a linear position.
		We have the opposite method for going back.

		:param x: The X coord in the grid
		:type x: int
		:param y: The Y coord in the grid
		:type y: int
		'''

		pos = y * self.grid.divisions + x
		return pos


	def pos_to_grid( self, pos ):
		'''
		Take a position in our list and find the coordinate in
		the grid.
			
		:param pos: a position/index in the list
		:type pos: int
		'''
		x = pos % self.grid.divisions
		y = pos - x
		y = y / self.grid.divisions

		return x, y


	def time_passes( self, time_delta ):
		'''
		This is the data update call to all the lifes.  Any of
		the rules that need to be followed will be followed here
		in some way
			
		:param time_delta: The time it took to get to this update.
		:type time_delta: float
		'''

		idx, all_life = self.grid.get_all_life()
		if all_life:
			for _i, life in enumerate( all_life ):
				life.decrement()
				if life.life == 0:
					self.grid.kill_life( idx[ _i ] )


class Grid():
	'''
	The Grid is what holds all of the lifes.  It creates/kills and 
	knows where the lifes are.	
	
	:param divisions: The number of x * y is the number of entries
	:type divisions: int
	'''

	def __init__( self, divisions ):
		self.divisions = divisions
		self.grid = [ None for x in range( self.divisions * self.divisions ) ]


	def add_life( self, pos, life ):  
		'''
		Add the created life to a position in the list.
			
		:param pos: The int position in the list
		:type pos: int
		:param life: A Life object
		:type life: Life
		'''

		self.grid[ pos ] = life
		

	def kill_life( self, pos ):
		'''
		Delete the life in this pos
		'''
		self.grid[ pos ] = None


	def get_all_life( self ):
		indexs = [ ]
		lifes = [ ]
		for idx, life in enumerate( self.grid ):
			if life:
				indexs.append( idx )
				lifes.append( life )

		if indexs:
			return indexs, lifes
		else:
			return None, None

	
	def get_neighbors_of_position( self, pos ):
		pass
# 		n_pos = self.get_north( pos )
# 		ne_pos = self.get_north_east( pos )
# 		e_pos = self.get_east( pos )
# 		se_pos = self.get_south_east( pos )
# 		s_pos = self.get_south( pos )

	def get_north( self, pos ):
		new_pos = pos - self.divisions
		if new_pos >= 0:
			return new_pos
		else:
			return None


	def get_north_east( self, pos ):
		pos = self.get_north( pos )
		if pos:
			return self.get_east( pos )


	def get_north_west( self, pos ):
		pos = self.get_north( pos )
		if pos:
			return self.get_west( pos )


	def get_south( self, pos ):
		new_pos = pos + self.divisions
		if new_pos < len( self.grid ):
			return new_pos
		else:
			return None


	def get_south_east( self, pos ):
		pos = self.get_south( pos )
		if pos:
			return self.get_east( pos )


	def get_south_west( self, pos ):
		pos = self.get_south( pos )
		if pos:
			return self.get_west( pos )


	def get_west( self, pos ):

		# This is the left most edge
		if pos % self.divisions == 0:
			return None

		new_pos = pos - 1
		return new_pos

	def get_east( self, pos ):
		if pos == len( self.grid ):
			return None

		# Modding against divisions resulting in one less than
		# divisions means we are next to the edge.
		if ( pos % self.divisions ) == ( self.divisions - 1 ):
			return None

		new_pos = pos + 1
		return new_pos


class Life():
	"""
	A life-form that generates more of itself based on rules.  It also
	has a lifespan.  
	
	TODO : I'm not sure if the life should know about neighbors, or if the 
	grid should know.  The Grid does know about neighbors so it at least does
	that.
	"""
	MAX_LIFE = 4 

	def __init__( self ):
		self.life = 4 

	def decrement( self ):
		'''
		Decrement the life.  This doesn't account for time right now
		just a negative	
		'''
		self.life -= 1
		self.life = max( [ self.life, 0 ] )

