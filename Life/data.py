
	
	
class Data( ):
	def __init__( self, div ):
		self.grid = Grid( div )
		self.life = Life

	
	def create_life( self, x, y ):
		pos = self.grid_to_pos(x, y)
		life = self.life( )
		self.grid.grid[ pos ] = life

	
	def grid_to_pos( self, x, y ):
		pos = y * self.grid.divisions + x
		return pos

	
	def pos_to_grid( self, pos ):
		x = pos % self.grid.divisions
		y = pos - x 
		y = y / self.grid.divisions
		
		return x, y
		
		

class Grid( ):
	def __init__( self, divisions ):
		self.divisions = divisions
		self.grid = [ None for x in range( self.divisions + self.divisions ) ]
		
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
		new_pos = pos - 1
		if new_pos >= 0:
			return new_pos
		else:
			return None
		
	def get_east( self, pos ):
		new_pos = pos + 1
		if new_pos < len( self.grid ):
			return new_pos
		else:
			return None
		
		
class Life( ):
	"""
	A life-form that generates more of itself based on rules.  It also 
	has a lifespan.
	"""

	def __init__( self ):
		self.life = 10
		
	