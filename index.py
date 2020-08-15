import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from app import dbc
import dash

from app import app
from apps import Morning, Afternoon, Night, home, functions as fx, Morning_Sorting, Afternoon_Sorting,Night_Sorting, Shuttle,Morning_Fill,Afternoon_Fill,Night_Fill

app.layout = html.Div([

    html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.Button("Summary",id="collapse-button-summary",className="mb-3",color="success",size='lg',href='/apps/home'),
                dbc.Button("Morning",id="collapse-button-morning",className="mb-3",color="success",size='lg'),
                dbc.Button("Afternoon",id="collapse-button-afternoon",className="mb-3",color="success",size='lg'),
                dbc.Button("Night",id="collapse-button-night",className="mb-3",color="success",size='lg'),
                dbc.Button("Others",id="collapse-button-shuttle",className="mb-3",color="success",size='lg',href='/apps/Shuttle'),
                    ],
            brand="Ambient Mezzanine",
            brand_href="",
            color="success",
            dark=True,
            style={'font-size': '20px'},
        ),
        dbc.Collapse(dbc.Card(dbc.CardBody(dbc.Nav([dbc.NavItem(dbc.Button("Pulling", outline=True, color="success", className="mr-1",size='lg',href="/apps/Morning")),
                                                    dbc.NavItem(dbc.Button("Sorting", outline=True, color="success", className="mr-1",size='lg',href='/apps/Morning_Sorting')),
                                                    dbc.NavItem(dbc.Button("Fill Active", outline=True, color="success", className="mr-1",size='lg',href='/apps/Morning_Fill')),
                                                    dbc.NavItem(html.H3("\t\t Morning")),
                                                ]))),
                                                    id="collapse-morning",
                                                ),
        dbc.Collapse(dbc.Card(dbc.CardBody(dbc.Nav([dbc.NavItem(dbc.Button("Pulling", outline=True, color="success", className="mr-1",size='lg',href="/apps/Afternoon")),
                                                    dbc.NavItem(dbc.Button("Sorting", outline=True, color="success", className="mr-1",size='lg',href='/apps/Afternoon_Sorting')),
                                                    dbc.NavItem(dbc.Button("Fill Active", outline=True, color="success", className="mr-1",size='lg',href='/apps/Afternoon_Fill')),
                                                    dbc.NavItem(html.H3("\t\t Afternoon")),
                                                ]))),
                                                    id="collapse-afternoon",
                                                ),
        dbc.Collapse(dbc.Card(dbc.CardBody(dbc.Nav([dbc.NavItem(dbc.Button("Pulling", outline=True, color="success", className="mr-1",size='lg',href="/apps/Night")),
                                                    dbc.NavItem(dbc.Button("Sorting", outline=True, color="success", className="mr-1",size='lg',href='/apps/Night_Sorting')),
                                                    dbc.NavItem(dbc.Button("Fill Active", outline=True, color="success", className="mr-1",size='lg',href='/apps/Night_Fill')),
                                                    dbc.NavItem(html.H3("\t\t Night")),
                                                ]))),
                                                    id="collapse-night",
                                                ),
        dbc.Collapse(dbc.Card(dbc.CardBody(dbc.Nav( html.H3('Summary')))),id="collapse-summary"),
        dbc.Collapse(dbc.Card(dbc.CardBody(dbc.Nav( html.H3('Shuttle')))),id="collapse-shuttle"),
        ]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
                    ])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Morning':
        return Morning.layout()
    elif pathname == '/apps/Afternoon':
        return Afternoon.layout()
    elif pathname == '/apps/Night':
        return Night.layout()
    # elif pathname == '/apps/home':
    #     return home.layout
    elif pathname == '/apps/Morning_Sorting':
        return Morning_Sorting.layout()
    elif pathname == '/apps/Afternoon_Sorting':
        return Afternoon_Sorting.layout()
    elif pathname == '/apps/Night_Sorting':
        return Night_Sorting.layout()
    elif pathname == '/apps/Shuttle':
        return Shuttle.layout()
    elif pathname == '/apps/Morning_Fill':
        return Morning_Fill.layout()
    elif pathname == '/apps/Afternoon_Fill':
        return Afternoon_Fill.layout()
    elif pathname == '/apps/Night_Fill':
        return Night_Fill.layout()
    else: 
        return home.layout()

@app.callback([Output("collapse-morning", "is_open"),Output("collapse-afternoon", "is_open"),Output("collapse-night", "is_open"),Output("collapse-summary", "is_open"),Output("collapse-shuttle", "is_open")],
    [Input("collapse-button-morning", "n_clicks"),Input("collapse-button-afternoon", "n_clicks"),Input("collapse-button-night", "n_clicks"),Input("collapse-button-summary", "n_clicks"),Input("collapse-button-shuttle", "n_clicks")],
    [State("collapse-morning", "is_open"),State("collapse-afternoon", "is_open"),State("collapse-night", "is_open"),State("collapse-summary", "is_open"),State("collapse-shuttle", "is_open")])

def toggle_accordion(n1, n2, n3,n4,n5, is_open1, is_open2, is_open3,is_open4,is_open5):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False,False,False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "collapse-button-morning" and n1:
        return not is_open1, False, False,False,False
    elif button_id == "collapse-button-afternoon" and n2:
        return False, not is_open2, False,False,False
    elif button_id == "collapse-button-night" and n3:
        return False, False, not is_open3,False,False
    elif button_id == "collapse-button-night" and n3:
        return False, False, not is_open3,False,False
    elif button_id == "collapse-button-summary" and n4:
        return False, False, False,not is_open4,False
    elif button_id == "collapse-button-shuttle" and n5:
        return False, False, False,False,not is_open5
    
    return False, False, False,False, False
    


if __name__ == '__main__':
    app.run_server(debug=False,port=8000,host='0.0.0.0')
