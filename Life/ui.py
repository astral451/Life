

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
	return QtWidgets.QApplication.instance( )


class Run_Thread( threading.Thread ):

	def __init__( self, method_to_execute ):
		super( ).__init__( )
		self.method_to_execute = method_to_execute
		self.keep_going = False
		self.duration = 1


	def run( self ):
		self.keep_going = True
		
		while self.keep_going:
			self.method_to_execute( )
			time.sleep( self.duration )

		
	
	def stop( self ):
		self.keep_going = False
		
		

class App( QtWidgets.QApplication ):
	def __init__( self, args ):
		super( ).__init__( args )
		
	def close( self ):
		self.quit( )
		


class Window( QtWidgets.QMainWindow ):
	def __init__( self ):
		super( ).__init__( )
		
		self.initUI( )
		

	def menu_setup( self ):
		exit_act = QtWidgets.QAction( QtGui.QIcon( 'exit.png' ), '&Exit', self )
		exit_act.setShortcut( 'Ctrl+Q' )
		exit_act.setStatusTip( 'Exit Application' )
		exit_act.triggered.connect( self._close )
		
		view_act = QtWidgets.QAction( 'View status bar', self, checkable = True )
		view_act.setStatusTip( 'View Status bar' )
		view_act.setChecked( True )
		view_act.triggered.connect( self.toggle_menu )
		
		menu_bar = self.menuBar( )
		file_menu = menu_bar.addMenu( '&File' )
		file_menu.addAction( exit_act )
		view_menu = menu_bar.addMenu( '&View' )
		view_menu.addAction( view_act )

		
	def initUI( self ):
		QtWidgets.QToolTip.setFont( QtGui.QFont( 'SansSerif', 10 ) )
		
		self.setToolTip( 'This is a <b>QWidget</b> widget' )
		
		btn = QtWidgets.QPushButton( 'Button', self )
		btn.setToolTip( 'This is a <b>QPushButton</b> widget' )
		btn.resize( btn.sizeHint( ) )
		btn.move( 10, 50 )
		
		close = QtWidgets.QPushButton( 'Quit', self )
		close.clicked.connect( self._close )
		close.resize( close.sizeHint( ) )
		close.move( 10, 80 )
		
		self.setGeometry( 200, 200, 512, 512 )
		self.setWindowTitle( "Life" )
		self.setWindowIcon( QtGui.QIcon( '..\web.png' ) )
		
		self.statusbar = self.statusBar( )
		self.statusbar.showMessage( 'Ready' )
		self.menu_setup( )

		self.show( )

	def _close( self ):
		event = QtGui.QCloseEvent( )
		self.statusBar( ).showMessage( 'close?' )
		app = get_top_app( )
		app.sendEvent( app, event )

		
	def closeEvent( self, event ):
		
		reply = QtWidgets.QMessageBox.question( self, 
												'Message', 
												"Are you sure to quit?",
												QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
												QtWidgets.QMessageBox.No )
		if reply == QtWidgets.QMessageBox.Yes:
			event.accept( )
		else:
			event.ignore( )

	
	def toggle_menu( self, state ):
		if state:
			self.statusbar.show( )
			self.statusbar.showMessage( 'Ready' )
		else:
			self.statusbar.hide( )
		
# 		self.update( )


class Top_Window( QtWidgets.QWidget ):
	def __init__( self ):
		super( ).__init__( )
		
		self.setWindowTitle( "Life" )
		self.setGeometry( 200, 200, 512, 512 )
		layout = QtWidgets.QGridLayout( )
		self.grid = Grid( )
		layout.addWidget( self.grid )
		
		self.thread = Run_Thread( self.on_thread_update )
		
		self.setLayout( layout )
		self.thread.start( )
	

	def on_thread_update( self ):
		paint_event = QtGui.QPaintEvent( self.rect( ) )
		app = get_top_app( )
		app.sendEvent( self, paint_event )
		self.grid.update( )

		
	def closeEvent( self, event ):
		
		reply = QtWidgets.QMessageBox.question( self, 
												'Message', 
												"Are you sure to quit?",
												QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
												QtWidgets.QMessageBox.No )
		if reply == QtWidgets.QMessageBox.Yes:
			self.thread.stop( )
			event.accept( )
		else:
			event.ignore( )


	

class Grid( QtWidgets.QWidget ):
	def __init__( self ):
		super( ).__init__( )
		
		font = self.font( )
		font.setPixelSize( 10 )	
		self.setFont( font )
		
		self.grid_size = 20 
		self.data = data.Data( self.grid_size )
		
		self.setMouseTracking( True )
		
	def mousePressEvent(self, event ):
		x = event.x( )
		y = event.y( )
		
		red_x = int( x / self.grid_size )
		red_y = int( y / self.grid_size )

		# width/height of each cell
		subdiv_x = self.size( ).width( ) / self.grid_size
		subdiv_y = self.size( ).height( ) / self.grid_size

		test_x = int( x / subdiv_x )
		test_y = int( y / subdiv_y )

	
		pos = self.data.grid_to_pos( test_x, test_y )
		print( '( {0},{1} ) : {2}'.format( test_x, test_y, pos ) )
# 		self.data.create_life( red_x, red_y )
		
		return QtWidgets.QWidget.mousePressEvent(self, event )


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
		painter.fillRect( rect, QtGui.QBrush( QtCore.Qt.white ) )
		
		self.draw_grid( painter )
		
		
		

if __name__ == "__main__":
	
	app = App( sys.argv )
	w = Top_Window( )
	w.show( )
	
	sys.exit( app.exec_( ) )