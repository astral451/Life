'''
Use this to graph the data over time. Currently uses Google charts to
make an HTML file.  Example HTML is in this doc
Created on Jan 5, 2019

@author: nathan
'''

import os
import const

top_html  = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart', 'line' ]});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([

"""

bottom_html = """			
        ]);

        var options = {
          title: 'Conways Game of Life Graph',
          curveType: 'line',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 1200px; height: 600px"></div>
  </body>
</html>"""


def create_chart( life_log ):
	"""
	Create a chart.html file that follows the google chart notations.  It's used
	to display the history and values happening while processing all the lives.
	"""

	lives = life_log.get( 'lives' )
	decrements = life_log.get( 'decrements' )
	deaths = life_log.get( 'deaths' )
	creates = life_log.get( 'creates' )
	
	string = "[ 'Tick', 'Lives', 'Decrements', 'Deaths', 'Creates' ],"
	row_template = '\t[{tick},	{live},	{decrement},	{death},	{create}]'
	for idx in range( len( lives ) ):
		life = lives[ idx ]
		dec = decrements[ idx ]
		det = deaths[ idx ]
		cre = creates[ idx ]
		line = row_template.format( tick = idx, live = life, decrement = dec, death = det, create = cre )
		if idx == 0:
			string += '\n{0}'.format( line )
		else:
			string += ',\n{0}'.format( line )

# 	final_html = html_example.format( DATA = string )
	final_html = top_html + '\n{0}\n'.format( string ) + bottom_html

	# Make sure the directory is there, then write the chart.html
	if not os.path.exists( os.path.dirname( const.CHART_FILE_NAME ) ):
			os.mkdir( os.path.dirname( const.CHART_FILE_NAME ) )
	
	with open( const.CHART_FILE_NAME, 'w' ) as fio:
		fio.write( final_html )

	print( const.CHART_FILE_NAME )

	
