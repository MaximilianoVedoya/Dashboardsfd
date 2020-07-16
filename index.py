import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import Morning, Afternoon, Night, home, functions as fx

#update the database
fx.get_data()  
fx.initializer(3,-1,-1)

app.layout = html.Div([html.H1(dcc.Link('HOME', href='/apps/home'),style={'text-align':'center'}),html.H2([dcc.Link('Morning /', href='/apps/Morning'),dcc.Link(' Afternoon /', href='/apps/Afternoon'),dcc.Link(' Night /', href='/apps/Night')],
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
    elif pathname == '/apps/home':
        return home.layout
    else: 
        return 'To be continued'

if __name__ == '__main__':
    app.run_server(debug=False,port=8000,host='0.0.0.0')