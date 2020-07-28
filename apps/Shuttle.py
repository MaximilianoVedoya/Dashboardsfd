from datetime import date
import datetime
import time 
import pandas as pd
import numpy as np 
import dash
import dash_table
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
from apps import functions as fx

import datetime
date=datetime.date.today()
date=str(date.strftime('%m/%d/%Y'))[:6]+str(date.strftime('%m/%d/%Y'))[-2:]
main=fx.shuttle_read(date)[0].iloc[:,1:]
fig=fx.shuttle_read(date)[1]


def layout(): 
    return (
        html.Div(
        [   
            html.Div(dcc.DatePickerSingle(id='my-date-picker-single',
                                                min_date_allowed=datetime.datetime(2020,7,17),
                                                max_date_allowed=datetime.date.today()-datetime.timedelta(days=0),
                                                initial_visible_month=datetime.date.today(),
                                                date=str(datetime.date.today())
                                                )),
            html.H1('Shuttle stats',style={'float': 'center','text-align':'center'}),
            html.H2(id='time_update',children=''),
            html.Div([dash_table.DataTable( id='main_table',
                                            columns=[{"name": i, "id": i} for i in main.columns],
                                            data=main.to_dict('records'),
                                            editable=False,
                                            sort_action="native",
                                            column_selectable="single",
                                            selected_columns=[],
                                            selected_rows=[],
                                            page_action="native",
                                            page_current= 0,
                                            page_size= 100,
                                            style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'},
                                            style_data_conditional=
                                                [ 
                                                    {
                                                        'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 400'.format(x)},
                                                        'background_color': '#B3E577',
                                                    } for x in main.columns

                                                ]
                                                +
                                                [
                                                    {
                                                        'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 350 && {{{0}}} <400'.format(x)},
                                                        'background_color': '#E0ED4B',
                                                    } for x in main.columns
                                                ]
                                                +
                                                [
                                                    {
                                                        'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 350'.format(x)},
                                                        'background_color': '#F78B54',
                                                    } for x in main.columns
                                                ]
                                                +
                                                [
                                                    {
                                                        'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                        'background_color': '#fafcfa',
                                                    } for x in main.columns
                                                ]
                                                +
                                                
                                                [
                                                    {
                                                        'if': {'column_id': 'ilpn'},'fontWeight': 'bold',
                                                    } 
                                                ]
                                            ),
                  
                        ],style={'width':'70%'}),
            html.Div(dcc.Graph(id='rates_graph',figure=fig,style={'width': '65%'})),
        ])
    )


@app.callback(Output('main_table', 'data'),
    [Input('my-date-picker-single', 'date')])

def select_date(date):
       date=pd.Timestamp(date) 
       date=str(date.strftime('%m/%d/%Y'))[:6]+str(date.strftime('%m/%d/%Y'))[-2:]
       main=fx.shuttle_read(date)[0].iloc[:,1:]
       data=main.to_dict('records')
       return data

@app.callback(Output('rates_graph','figure'),
    [Input('my-date-picker-single', 'date')])

def update_graph(date):
       date=pd.Timestamp(date) 
       date=str(date.strftime('%m/%d/%Y'))[:6]+str(date.strftime('%m/%d/%Y'))[-2:]
       fig=fx.shuttle_read(date)[1]
       return fig