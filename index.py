import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import Morning, Afternoon, Night, home, functions as fx, Morning_Sorting, Afternoon_Sorting,Night_Sorting, Shuttle

app.layout = html.Div([
                       html.Div([
                                html.H1(dcc.Link('Ambient Shuttle', href='/apps/Shuttle')),
                                html.Br(),  
                                html.H1(dcc.Link('Ambient Mezzanine', href='/apps/home')),
                                html.H2(['Morning',
                                            dcc.Link(' (Pulling |', href='/apps/Morning'),
                                            dcc.Link(' Sorting |', href='/apps/Morning_Sorting'),
                                            dcc.Link(' Fill active)     ', href='/apps/Mornign_Putaway'),
                                            'Afternoon',
                                            dcc.Link(' (Pulling |', href='/apps/Afternoon'),
                                            dcc.Link(' Sorting |', href='/apps/Afternoon_Sorting'),
                                            dcc.Link(' Fill active)     ', href='/apps/Afternoon_Putaway'),
                                            'Night',
                                            dcc.Link(' (Pulling |', href='/apps/Night'),
                                            dcc.Link(' Sorting |', href='/apps/Night_Sorting'),
                                            dcc.Link(' Fill active)     ', href='/apps/Night_Putaway')
                                        ]),
                                html.Br(),        
                                ],style={'text-align':'center','background-color':'#d0efca'}),
                        
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
        return home.layout()
    elif pathname == '/apps/Morning_Sorting':
        return Morning_Sorting.layout
    elif pathname == '/apps/Afternoon_Sorting':
        return Afternoon_Sorting.layout
    elif pathname == '/apps/Night_Sorting':
        return Night_Sorting.layout
    elif pathname == '/apps/Shuttle':
        return Shuttle.layout()
    else: 
        return 'To be continued'
if __name__ == '__main__':
    app.run_server(debug=False,port=8000,host='0.0.0.0')