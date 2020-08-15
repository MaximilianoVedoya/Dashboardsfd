import datetime 
from datetime import date 
import time
import pandas as pd
import numpy as np 
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from app import app
from app import dbc
import dash_bootstrap_components as dbc
from apps import functions as fx

reference='summary'
refreshing_time=1*60*1000 #millisecods
input_date=datetime.date.today()

summary=fx.summary_get_main(input_date)


def layout ():
    return (
            html.Div(
                [   
                    html.H1('Summary',style={'text-align':'center'}),
                    html.H2(id=reference+'time_update',children='',style={'text-align':'center'}),
                    html.Div(
                        [
                            html.Div(dcc.DatePickerSingle(id=reference+'my-date-picker-single',
                                                        min_date_allowed=datetime.datetime(2020,8,4),
                                                        max_date_allowed=datetime.date.today(),
                                                        initial_visible_month=datetime.date.today(),
                                                        date=str(datetime.date.today())
                                                        )),
                            dash_table.DataTable(   id=reference+'summary_table',
                                                    columns=[{"name": i, "id": i} for i in summary.columns],
                                                    data=summary.to_dict('records'),
                                                    style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis','font_size': '22px','fontWeight': 'bold'},
                                                    style_data_conditional=
                                                            [
                                                                {
                                                                    'if': 
                                                                    {
                                                                        'filter_query': '{Difference} < 0',
                                                                        'column_id': ['Difference','Net Results','Expected Results']
                                                                    },
                                                                    'backgroundColor': 'tomato',
                                                                    'color': 'white'
                                                                }
                                                            ]
                                                            +
                                                            [
                                                                {
                                                                    'if': 
                                                                    {
                                                                        'filter_query': '{Difference} >= 0',
                                                                        'column_id': ['Difference','Net Results','Expected Results']
                                                                    },
                                                                    'backgroundColor': 'green',
                                                                    'color': 'white'
                                                                }
                                                            ]
                                                )
                        ]),
                    html.Div(dcc.Interval(
                        id=reference+'interval-tables',
                        interval=refreshing_time, # in milliseconds
                        n_intervals=0)),
                    
                ],style={'margin-left':'10%','margin-right':'10%'})
            )

@app.callback(Output(reference+'summary_table', 'data'),
    [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def table_date_retriever(date,n_intervals):
    summary=fx.summary_get_main(date)
    data=summary.to_dict('records')
    return data