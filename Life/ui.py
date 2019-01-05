
"""
The Main UI of this 'game'  It's an idea of starting/stopping the game
of life.  https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

All ui and drawing happens here.  data.py is just the Life objects and
their grid.
"""

"""
http://zetcode.com/gui/pyqt5/firstprograms/
"""

import sys
import threading
import time

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import data


def get_top_app( ):
	"""
	Get the top window through Qt method.
	"""
	
	return QtWidgets.QApplication.instance( )


class Run_Thread( threading.Thread ):
	"""
	The thread for automatically updating the UI.  This is periodic, but
	does NOT stop execution until the app closes.	
	"""

	def __init__( self, method_to_execute ):
		super( ).__init__( )
		self.method_to_execute = method_to_execute
		self.keep_going = False
		self.duration = 1 # duration to wait


	def run( self ):
		self.keep_going = True
		
		while self.keep_going:
			self.method_to_execute( )
			time.sleep( self.duration )

	
	def stop( self ):
		self.keep_going = False
		
		

class App( QtWidgets.QApplication ):
	"""
	A top level app, but really does nothing.  I may want to delete it.
	"""
	
	def __init__( self, args ):
		super( ).__init__( args )
		

	def close( self ):
		self.quit( )
		


class Top_Window( QtWidgets.QMainWindow ):
	"""
	Top most window, contains the menus and such.
	"""

	def __init__( self ):
		super( ).__init__( )
		self.setGeometry( 200, 200, 512, 512 )
		self.setWindowTitle( "Life" )

		self.grid_window = Grid_Window( )
		self.setCentralWidget( self.grid_window )

		self.statusbar = self.statusBar( )
		self.statusbar.showMessage( 'Paused' )
		self.menu_setup( )


	def menu_setup( self ):
		"""
		The menu for Pause and Play	
		"""
		play_act = QtWidgets.QAction( QtGui.QIcon( '.\_images\play.png' ), '&Play', self )
		play_act.setShortcut( 'Ctrl+P' )
		play_act.setStatusTip( 'Play' )
		play_act.triggered.connect( self._play )
		
		pause_act = QtWidgets.QAction( QtGui.QIcon( '.\_images\pause.png' ), 'P&ause', self )
		pause_act.setShortcut( 'Ctrl+A' )
		pause_act.setStatusTip( 'Pause' )
		pause_act.triggered.connect( self._pause )
		
		reset_act = QtWidgets.QAction( QtGui.QIcon( '.\_images\reset.png' ), '&Reset', self )
		reset_act.setShortcut( 'Ctrl+R' )
		reset_act.setStatusTip( 'Reset Grid' )
		reset_act.triggered.connect( self._reset )

		menu_bar = self.menuBar( )
		menu_bar.addAction( play_act )
		menu_bar.addAction( pause_act )
		menu_bar.addAction( reset_act )


	def _pause( self ):
		"""
		sets the grids thread to pause, or rather to just stop time_passes 
		"""
		self.statusbar.showMessage( 'Pause' )
		self.grid_window.run = False
		
		
	def _play( self ):
		"""
		sets the grids thread to play, or rather to just start time_passes 
		"""
		self.statusbar.showMessage( 'Play' )
		self.grid_window.run = True 

	
	def _reset( self ):
		# pause before reset
		self._pause( )
		self.statusbar.showMessage( 'Reset' )
		self.grid_window.grid.reset( )

	def closeEvent( self, event ):
		"""
		Controls the close event, prompting the user if they want to close.
		This also stops the running Thread if the user says Yes.
		"""
		reply = QtWidgets.QMessageBox.question( self, 
												'Message', 
												"Are you sure to quit?",
												QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
												QtWidgets.QMessageBox.No )
		if reply == QtWidgets.QMessageBox.Yes:
			self.grid_window.thread.stop( )
			event.accept( )
		else:
			event.ignore( )



class Grid_Window( QtWidgets.QWidget ):
	"""
	This window holds the Grid. This layer also holds the thread
	that is running. The widget is designed to keep updating the UI
	as it goes.  The grid itself is what draws however.	
	"""
	def __init__( self ):
		super( ).__init__( )
		
		layout = QtWidgets.QGridLayout( )
		self.grid = Grid( )
		layout.addWidget( self.grid )
		

		self.run = False
		self.thread = Run_Thread( self.on_thread_update )
		
		self.setLayout( layout )
		self.thread.start( )
	


	def on_thread_update( self ):
		"""
		The method being executed by our Thread object.  This is calling
		the UI update every {duration} from the thread.  All it does is
		create a PaintEvent and send it to the top level window and that
		cascades into the rest of the UI.  The only additional call is to
		the grid, and for it to update ( redraw in qt )
		"""
		self.time_passes( )

		paint_event = QtGui.QPaintEvent( self.rect( ) )
		app = get_top_app( )
		app.sendEvent( self, paint_event )
		self.grid.update( )

	
	def time_passes( self ):
		"""
		Time passes is method to calculate the duration of the wait
		and to call a time_passes on the underlying data.  This is
		coming from the UI so the Data is responsible for knowing
		what to do with the duration.  
		
		:**TODO**:
			* A flaw in this code is that we are tracking the delta even while paused.
			I think this is possibly going to cause problems when the Lifes 
			are listening for real duration.  I'll need to find away to pause
			the advancement of time, not simply stop processing.

		"""
		current_time = time.clock( )
		if not hasattr( self, '_start_time' ):
			self._start_time = current_time 
		
		# update our lifes
		delta = current_time - self._start_time
		self._start_time = current_time
		if self.run:
			self.grid.data.time_passes( delta )

	

class Grid( QtWidgets.QWidget ):
	"""
	The grid is drawing the grid and any lifes that exist.  It does handle
	all visual updates.	
	"""
	def __init__( self ):
		super( ).__init__( )
		
		font = self.font( )
		font.setPixelSize( 10 )	
		self.setFont( font )
		
		# TODO : Need to externalize this
		self.grid_size = 20 
		self.data = data.Data( self.grid_size )
		
		self.setMouseTracking( True )
		

	def mousePressEvent(self, event ):
		"""
		Mouse events for clicking around the grid.  It does the math
		to figure out what grid square you are in.	
		"""
		x = event.x( )
		y = event.y( )
		
		# width/height of each cell
		subdiv_x = self.size( ).width( ) / self.grid_size
		subdiv_y = self.size( ).height( ) / self.grid_size

		test_x = int( x / subdiv_x )
		test_y = int( y / subdiv_y )

		self.data.create_life( test_x, test_y )
		
		# pass the mouse event along.
		return QtWidgets.QWidget.mousePressEvent(self, event )


	def draw_life( self, painter ):
		'''
		Draw the life, start by figuring out where it is in the grid. There
		is a sub-call to draw the square, but this is the starting point.
				
		:param painter:
		:type painter:
		'''


		idxs, lifes = self.data.grid.get_all_life( )

		subdiv_x = self.size( ).width( ) / self.grid_size
		subdiv_y = self.size( ).height( ) / self.grid_size
		
		if lifes:
			for idx, life in enumerate( lifes ) : 
				l_idx = idxs[ idx ]
				x, y = self.data.pos_to_grid( l_idx )
				pos_x = int( x * subdiv_x ) - 1 # TODO, better alignment
				pos_y = int( y * subdiv_y ) - 1
				end_x = int( pos_x + subdiv_x ) - 1
				end_y = int( pos_y + subdiv_y ) - 1

				start_point = QtCore.QPoint( pos_x, pos_y )
				end_point = QtCore.QPoint( end_x, end_y )
				
				self.draw_square( painter, start_point, end_point, life )

	
	def draw_square( self, painter, start_point, end_point, life ):
		# turn value into a color and clamp the value, just in case
		# Note I invert the value so it goes from black -> white
		life_color = max( 0 , min( 255, 255 * ( ( life.MAX_LIFE - life.life ) / life.MAX_LIFE ) ) )


		color = QtGui.QColor( life_color, life_color, life_color, 255 )
		painter.setBrush( QtGui.QBrush( color ) )
		painter.drawRect( QtCore.QRect( start_point, end_point ) )

	

	def draw_grid( self, painter ):
		rect = self.rect( )
		
		x, y, size_x, size_y = rect.getCoords( )
		sub_x = size_x / self.grid_size
		sub_y = size_y / self.grid_size
		
		painter.setPen( QtGui.QPen( QtGui.QColor( "black" ) ) )
		for i in range( self.grid_size ):

			painter.drawLine( i * sub_x, 	y, 			i * sub_x, 	size_y  )
			painter.drawLine( x, 			i * sub_y, 	size_x, 		i * sub_y  )


	def paintEvent( self, event ):

		painter = QtGui.QPainter( self )
		painter.setRenderHint( QtGui.QPainter.Antialiasing )
		rect = event.rect( )
		painter.eraseRect( rect )
		painter.fillRect( rect, QtGui.QBrush( QtCore.Qt.white ) )
		
		self.draw_grid( painter )
		self.draw_life( painter )
		
		
	def reset( self ):
		self.data.reset( )
		

if __name__ == "__main__":
	
	app = App( sys.argv )
	w = Top_Window( )
	w.show( )
	
	sys.exit( app.exec_( ) )