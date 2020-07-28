import datetime 
from datetime import date 
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
from apps import Afternoon, Morning,Night, functions as fx
from app import app
import re

n_shift=Night.results_table
m_shift=Morning.results_table
a_shift=Afternoon.results_table
date_=fx.date_reader()
total= fx.summary(n_shift,m_shift,a_shift,date_)
pulling_graph=fx.graphs(date_)[0]
sorting_graph=fx.graphs(date_)[1]
def layout():
        return (
                html.Div(dcc.DatePickerSingle(id='my-date-picker-single',
                                              min_date_allowed=datetime.datetime(2020,7,12),
                                              max_date_allowed=datetime.date.today()-datetime.timedelta(days=0),
                                              initial_visible_month=datetime.date.today(),
                                              date=str(datetime.date.today())
                                              )),
                html.H1('Summary',style={'float': 'center','text-align':'center'},id='summary'),
                # html.H2('Pulling',style={'float': 'center','text-align':'center'}),
                html.Div([
                        # dash_table.DataTable(
                        #     id='main_table_home',
                        #     columns=[{"name": i, "id": i} for i in total.columns],
                        #     data=total.to_dict('records'),
                        #     editable=False,
                        #     sort_action="native",
                        #     column_selectable="single",
                        #     selected_columns=[],
                        #     selected_rows=[],
                        #     page_action="native",
                        #     page_current= 0,
                        #     page_size= 100,
                        #     style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'},
                        #     ),
                        dcc.Interval(
                                    id='interval-data',
                                    interval=5*60*1000, # in milliseconds
                                    n_intervals=0
                                    )
                        ],style={'text-align':'center','width':'100%','float': 'center'}),

                html.Div(dcc.Graph(id='Pulling_graph',figure=pulling_graph),style={'width': '75%'}),
                
                # html.H2('Sorting',style={'float': 'center','text-align':'center'}),
                html.Div(dcc.Graph(id='Sorting_graph',figure=sorting_graph),style={'width': '75%'}),
                
                )


@app.callback(Output('summary', 'children'),
    [Input('my-date-picker-single', 'date')])

def save_date(date):
        def save_object(obj, filename):
            import pickle
            with open(filename, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        save_object(date,'date.pckl')
    
@app.callback(Output('date-picker', 'children'),
    [Input('my-date-picker-single', 'date')])

def update_date(date):
    return str(date)[5:10]

@app.callback(Output('Pulling_graph', 'figure'),
    [Input('my-date-picker-single', 'date')])

def update_pulling_graph(date):
    date_=fx.date_reader()
    return fx.graphs(date_)[0]

@app.callback(Output('Sorting_graph', 'figure'),
    [Input('my-date-picker-single', 'date')])

def update_pulling_graph(date):
    date_=fx.date_reader()
    return fx.graphs(date_)[1]

