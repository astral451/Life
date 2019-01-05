'''
A set of methods, that define the rules for the live and
dead lifes in the system.  The methods are used to evaluate
whether a life should be created or decremented.

Created on Jan 4, 2019

@author: nathan.turner
'''

def simple_rule( lives, empties ):
	
	lives_to_decrement = [ ]
	lives_to_create = [ ]
	
	
	for life in lives:
		lives_to_decrement.append( life )
		
	return lives_to_decrement, lives_to_create
		

def standard_conway_rules( lives, empties ):
	'''
	These are the standard rules based on this website:
	https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

	Any live cell with fewer than two live neighbors dies, as if by underpopulation.
	Any live cell with two or three live neighbors lives on to the next generation.
	Any live cell with more than three live neighbors dies, as if by overpopulation.
	Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.	

	:param lives: A list of live neighbor objects
	:type lives: list[data.Neighborhood]
	:param emtpies: A list of empty neighbor objects
	:type emtpies: list[ data.Neighborhood]
	'''
	
	
	lives_to_decrement = [ ]
	lives_to_create = [ ]
	
	for life in lives: # type: data.Life
		life_neighbors = [ life.get_data_in_pos( dir )[ 'life' ] for dir in life.DIRECTIONS if life.get_data_in_pos( dir )[ 'life' ] ]
		life_count = len( life_neighbors )
		
		if life_count < 2:
			lives_to_decrement.append( life )
		elif life_count > 3:
			lives_to_decrement.append( life )
			
			
	for life in empties:
		life_neighbors = [ life.get_data_in_pos( dir )[ 'life' ] for dir in life.DIRECTIONS if life.get_data_in_pos( dir )[ 'life' ] ]
		life_count = len( life_neighbors )
		
		if life_count == 3:
			lives_to_create.append( life )
	
	return lives_to_decrement, lives_to_create

		
		