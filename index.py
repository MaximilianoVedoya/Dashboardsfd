import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import Morning, Afternoon, Night


#definition of shifts 
morning=[('4:00','5:00'),('5:00','6:00'),('6:00','7:00'),('7:00','8:00'),
                ('8:00','9:00'),('9:00','10:00'),('10:00','11:00'),('11:00','12:00')]
afternoon=[('12:00','13:00'),('13:00','14:00'),('14:00','15:00'),('15:00','16:00'),
                ('16:00','17:00'),('17:00','18:00'),('18:00','19:00'),('19:00','20:00')]
night=[('20:00','21:00'),('21:00','22:00'),('22:00','23:00'),('23:00','0:00'),
                ('0:00','1:00'),('1:00','2:00'),('2:00','3:00'),('3:00','4:00')]


app.layout = html.Div([html.H3([dcc.Link('Morning /', href='/apps/Morning'),dcc.Link(' Afternoon /', href='/apps/Afternoon'),dcc.Link(' Night /', href='/apps/Night')],
style={'text-align':'center'}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Morning':
        return Morning.layout
    elif pathname == '/apps/Afternoon':
        return Afternoon.layout
    elif pathname == '/apps/Night':
        return Night.layout
    else:
        return 'To be continued'

if __name__ == '__main__':
    app.run_server(debug=False,port=8000,host='0.0.0.0')
