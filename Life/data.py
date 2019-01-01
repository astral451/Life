

class Data():

	def __init__( self, div ):
		self.grid = Grid( div )
		self.life = Life

	def create_life( self, x, y ):
		pos = self.grid_to_pos( x, y )
		life = self.life()
		self.grid.add_life( pos, life )
# 		self.grid.grid[ pos ] = life

	def grid_to_pos( self, x, y ):
		pos = y * self.grid.divisions + x
		return pos

	def pos_to_grid( self, pos ):
		x = pos % self.grid.divisions
		y = pos - x
		y = y / self.grid.divisions

		return x, y

	def time_passes( self, time_delta ):
		idx, all_life = self.grid.get_all_life()
		if all_life:
			for _i, life in enumerate( all_life ):
				life.decrement()
				if life.life == 0:
					self.grid.kill_life( idx[ _i ] )


class Grid():

	def __init__( self, divisions ):
		self.divisions = divisions
		self.grid = [ None for x in range( self.divisions * self.divisions ) ]

	def add_life( self, pos, life ):
		self.grid[ pos ] = life
		
	def kill_life( self, pos ):
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

	def get_north( self, pos ):
		new_pos = pos - self.divisions
		if new_pos >= 0:
			return new_pos
		else:
			return None

	def get_south( self, pos ):
		new_pos = pos + self.divisions
		if new_pos < len( self.grid ):
			return new_pos
		else:
			return None

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
	"""
	MAX_LIFE = 10

	def __init__( self ):
		self.life = 10 

	def decrement( self ):
		self.life -= 1
		self.life = max( [ self.life, 0 ] )

