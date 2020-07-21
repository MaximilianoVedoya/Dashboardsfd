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
 
layout= html.Div([ 
                html.H1('Total Pulling',id='data_updater',style={'float': 'center','text-align':'center'}),
                # html.Div(id='date-picker',style={'float': 'center','align':'center'}),
                html.Div(dcc.DatePickerSingle( id='my-date-picker-single',
                                                # min_date_allowed=datetime.date.today()-datetime.timedelta(days=3),
                                                min_date_allowed=datetime.datetime(2020,7,12),
                                                max_date_allowed=datetime.date.today()-datetime.timedelta(days=0),
                                                initial_visible_month=datetime.date.today(),
                                                date=str(datetime.date.today())
                                                )),
                html.Div(dash_table.DataTable(
                                        id='main_table_home',
                                        columns=[{"name": i, "id": i} for i in total.columns],
                                        data=total.to_dict('records'),
                                        editable=False,
                                        sort_action="native",
                                        column_selectable="single",
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current= 0,
                                        page_size= 100,
                                        style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'},
                                    ),style={'text-align':'center','width':'100%','float': 'center'}
                    ),
                html.Div(dcc.Interval(
                            id='interval-data',
                            interval=5*60*1000, # in milliseconds
                            n_intervals=0))
                ])

@app.callback(Output('main_table_home', 'data'),
    [Input('my-date-picker-single', 'date')])

def update_overall_table(date):
    try:
        def save_object(obj, filename):
            import pickle
            with open(filename, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        save_object(date,'date.pckl')
        shifts=['Night shift','Morning shift','Afternoon shift']
        temp_=list()
        for shift in shifts:
            file_name=str(date)[5:10]+shift+'.xlsx'
            df=fx.main_table(file_name)
            temp_.append(fx.get_results_table(file_name,df))
        df=fx.summary(temp_[0],temp_[1],temp_[2],date)
        data=df.to_dict('records')
        return data
    except:
        return total.to_dict('records')


@app.callback(Output('date-picker', 'children'),
    [Input('my-date-picker-single', 'date')])

def update_date(date):
    return str(date)[5:10]


# @app.callback(Output('data_updater', 'data'),
#               [Input('interval-data', 'n_intervals')])

# def update_database(n_intervals):
#     fx.get_data()
#     fx.initializer(1,-1,-1)


