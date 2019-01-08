'''
Set of constants that control the Life Settings.  Grid Size, duration, 
MAX_LIFE, etc. will be controlled from here. This is set up so we can
set the UI controlled values.


Created on Jan 5, 2019

@author: nathan
'''

import os



MAX_LIFE 			= 1 
GRID_SUBDIV 		= 20
STEP_DURATION 		= .05
DRAW_GRID			= False 

POTENTIAL_RULES 	= { } # filled out in rules
RULE_TO_USE			= ''

CHART_FILE_NAME         = os.path.join( os.path.expanduser(  '~' ), 'life', 'chart.html' )

