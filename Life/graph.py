'''
Use this to graph the data over time. Currently uses Google charts to
make an HTML file.  Example HTML is in this doc
Created on Jan 5, 2019

@author: nathan
'''


top_html  = """
  <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
			var data = new google.visualization.DataTable();
			data.addColumn('number', 'Lives');
			data.addColumn('number', 'Decrements');
			data.addColumn('number', 'Deaths');
			data.addColumn('number', 'Creates');

			data.addRows([
"""

bottom_html = """			
			 ]);

        var options = {
          title: 'Conway Life Data',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('line'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 1200px; height: 500px"></div>
  </body>
</html>
"""


def create_chart( life_log ):
	lives = life_log.get( 'lives' )
	decrements = life_log.get( 'decrements' )
	deaths = life_log.get( 'deaths' )
	creates = life_log.get( 'creates' )
	
	string = ''
	row_template = '\t[{live},	{decrement},	{death},	{create}]'
	for idx in range( len( lives ) ):
		life = lives[ idx ]
		dec = decrements[ idx ]
		det = deaths[ idx ]
		cre = creates[ idx ]
		line = row_template.format( live = life, decrement = dec, death = det, create = cre )
		if idx == 0:
			string += '\n{0}'.format( line )
		else:
			string += ',\n{0}'.format( line )

# 	final_html = html_example.format( DATA = string )
	final_html = top_html + '\n{0}\n'.format( string ) + bottom_html
	
	filename = r'c:\chart.html'
	with open( filename, 'w' ) as fio:
		fio.write( final_html )

	print( filename )

	