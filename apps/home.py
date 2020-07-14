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

n_shift=Night.n_results_table
m_shift=Morning.m_results_table
a_shift=Afternoon.a_results_table

def get_summary(sum_):
    total=pd.DataFrame(columns=['Expected Results','Net Results','Difference'], index=pd.Series(range(4)))
    total
    total.iloc[0]=n_shift.iloc[0]
    total.iloc[1]=m_shift.iloc[0]
    total.iloc[2]=a_shift.iloc[0]
    reference=['Night','Morning','Afternoon','Total']
    total.insert(0,'Reference',reference)
    temp_=['Total']
    for column in ['Expected Results','Net Results','Difference']:
        temp_.append(sum_.iloc[0][column])
    total.iloc[3]=temp_
    return total
    
hour=int(time.ctime()[11:13])
if hour<=13:
    sum_=n_shift+m_shift
    total=get_summary(sum_)
if hour>13 and hour<=20:
    sum_=n_shift+m_shift+a_shift
    total=get_summary(sum_)



layout= html.Div([  html.H1('Total Pulling '+datetime.datetime.now().strftime("%m-%d"),style={'float': 'center','text-align':'center'}),
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
                                    ),style={'text-align':'center','width':'100%','table-layout':'fixed'}
                    ),
                    
                html.Div([dcc.DatePickerSingle( id='my-date-picker-single',
                                                min_date_allowed=datetime.date.today()-datetime.timedelta(days=3),
                                                max_date_allowed=datetime.date.today(),
                                                initial_visible_month=fx.date_reader(),
                                                date=str(fx.date_reader())
                                                ),
                html.Div(id='date-picker'),
                html.Div(   dcc.Interval(
                            id='interval-data',
                            interval=5*60*1000, # in milliseconds
                            n_intervals=0))
                        ])

                    ])

@app.callback(
    Output('date-picker', 'children'),
    [Input('my-date-picker-single', 'date')])
def update_output(date):
    string_prefix = 'You have selected: '
    if date is not None:
        import pickle 
        with open('date.pckl', 'wb') as f:  
            pickle.dump(date, f)
        f.close()
        date = datetime.datetime.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        return string_prefix + date_string


@app.callback(Output('main_table_home', 'data'),
              [Input('interval-data', 'n_intervals')])

def update_database(n_intervals):
    fx.get_data()    