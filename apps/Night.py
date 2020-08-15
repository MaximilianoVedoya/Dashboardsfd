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
from app import app
from apps import functions as fx
from app import dbc

schedule=['01AM', '02AM', '03AM', '08PM', '09PM', '10PM', '11PM', '12AM']
#reference is used infront of every single id of each one of the elements of the layout, to avoid duplicate callbacks
reference='Night shift'
#refreshing time establishes the amount of time by each callback
refreshing_time=1*60*1000 #millisecods


input_day=str(datetime.date.today())[5:10]
file_name=input_day+reference+'.xlsx'

#The following is to split the main table into 3 different sections 
main_table_1=fx.pulling_get_mains(file_name,'ranking_100')
main_table_2=fx.pulling_get_mains(file_name,'ranking_50')
main_table_total=fx.pulling_get_total(file_name)
results_table=fx.pulling_get_result_table(file_name)

#this is an auxiliary table to mark the columns for the style_data_conditional
columns=schedule
columns.append('Rate')

#this call the functions related with the graphs and an auxiliar table for perfomance graph
fig=fx.pulling_get_performance_fig(file_name)[0]
#this table combines all the users into one single table (repeating names) to show all of them into one single dropbox
merged_table=fx.pulling_get_performance_fig(file_name)[1]
fig2=fx.pulling_get_load_distribution_fig(file_name)

def layout ():
    return (
            html.Div(
                [   
                    html.H1('Pulling '+reference,style={'text-align':'center'}),
                    html.H2(id=reference+'time_update',children='',style={'text-align':'center'}),
                    html.Div(
                        [
                            html.Div(dcc.DatePickerSingle(id=reference+'my-date-picker-single',
                                                        min_date_allowed=datetime.datetime(2020,8,1),
                                                        max_date_allowed=datetime.date.today(),
                                                        initial_visible_month=datetime.date.today(),
                                                        date=str(datetime.date.today())
                                                        )),
                            dash_table.DataTable(   id=reference+'results_table',
                                                    columns=[{"name": i, "id": i} for i in results_table.columns],
                                                    data=results_table.to_dict('records'),
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
                                                ),
                            html.Br(),
                            dash_table.DataTable( id=reference+'main_table_1',
                                                    columns=[{"name": i, "id": i} for i in main_table_1.columns],
                                                    data=main_table_1.to_dict('records'),
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
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 80'.format(x)},
                                                                'background_color': '#B3E577',
                                                            } for x in columns

                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 60 && {{{0}}} <80'.format(x)},
                                                                'background_color': '#E0ED4B',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 60'.format(x)},
                                                                'background_color': '#F78B54',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                                'background_color': '#fafcfa',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        
                                                        [
                                                            {
                                                                'if': {'column_id': 'Rate'},'fontWeight': 'bold',
                                                            } 
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': 'usr'},'width':'20%',
                                                            } 
                                                        ]
                                                        +
                                                                                                    [
                                                            {
                                                                'if': {'column_id': 'Last Location'},'width':'10%',
                                                            } 
                                                        ]
                                                    
                                                ),
                            html.Br(),
                            dash_table.DataTable( id=reference+'main_table_2',
                                                    columns=[{"name": i, "id": i} for i in main_table_2.columns],
                                                    data=main_table_2.to_dict('records'),
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
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 50'.format(x)},
                                                                'background_color': '#B3E577',
                                                            } for x in columns

                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 40 && {{{0}}} <50'.format(x)},
                                                                'background_color': '#E0ED4B',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 40'.format(x)},
                                                                'background_color': '#F78B54',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                                'background_color': '#fafcfa',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        
                                                        [
                                                            {
                                                                'if': {'column_id': 'Rate'},'fontWeight': 'bold',
                                                            } 
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': 'usr'},'width':'20%',
                                                            } 
                                                        ]
                                                        +
                                                                                                    [
                                                            {
                                                                'if': {'column_id': 'Last Location'},'width':'10%',
                                                            } 
                                                        ]
                                                    ),
                            html.Br(),
                            dash_table.DataTable( id=reference+'main_table_total',
                                                    columns=[{"name": i, "id": i} for i in main_table_total.columns],
                                                    data=main_table_total.to_dict('records'),
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
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 500'.format(x)},
                                                                'background_color': '#B3E577',
                                                            } for x in columns

                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 400 && {{{0}}} <500'.format(x)},
                                                                'background_color': '#E0ED4B',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 400'.format(x)},
                                                                'background_color': '#F78B54',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                                'background_color': '#fafcfa',
                                                            } for x in columns
                                                        ]
                                                        +
                                                        
                                                        [
                                                            {
                                                                'if': {'column_id': 'Rate'},'fontWeight': 'bold',
                                                            } 
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': {'column_id': 'usr'},'width':'20%',
                                                            } 
                                                        ]
                                                        +
                                                                                                    [
                                                            {
                                                                'if': {'column_id': 'Last Location'},'width':'10%',
                                                            } 
                                                        ]
                                                    ),
                            html.Br(),
                        ]),
                    
                    html.Div(
                        dcc.Dropdown(id=reference+'merged_table_list',
                                        options=[{'label': i, 'value': i} for i in merged_table['usr']],
                                        value='Select PITO',
                                        placeholder='Select PITO',
                                        searchable=False,
                                        multi=False),style={'width':'30%'}),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id=reference+'rates_graph',figure=fig)),
                        dbc.Col(dcc.Graph(id=reference+'load_graph',figure=fig2)),
                        ]),
                    html.Div(dcc.Interval(
                        id=reference+'interval-tables',
                        interval=refreshing_time, # in milliseconds
                        n_intervals=0))
                ],style={'margin-left':'10%','margin-right':'10%'})\
            )
#these callbacks allows the user to go back and check on the results of the different dates. 

@app.callback(Output(reference+'main_table_1', 'data'),
    [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def table_date_retriever(date,n_intervals):
    input_day=str(date)[5:10]
    file_name=input_day+reference+'.xlsx'
    main_table_1=fx.pulling_get_mains(file_name,'ranking_100')
    data=main_table_1.to_dict('records')
    return data

@app.callback(Output(reference+'main_table_2', 'data'),
    [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def table_date_retriever(date,n_intervals):
    input_day=str(date)[5:10]
    file_name=input_day+reference+'.xlsx'
    main_table_2=fx.pulling_get_mains(file_name,'ranking_50')
    data=main_table_2.to_dict('records')
    return data

@app.callback(Output(reference+'main_table_total', 'data'),
    [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def table_date_retriever(date,n_intervals):
    input_day=str(date)[5:10]
    file_name=input_day+reference+'.xlsx'
    main_table_total=fx.pulling_get_total(file_name)
    data=main_table_total.to_dict('records')
    return data

@app.callback(Output(reference+'results_table', 'data'),
    [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def table_date_retriever(date,n_intervals):
    input_day=str(date)[5:10]
    file_name=input_day+reference+'.xlsx'
    results_table=fx.pulling_get_result_table(file_name)
    data=results_table.to_dict('records')
    return data

#This callback keep the droplist updated when changing dates in the date-picker
@app.callback(Output(reference+'merged_table_list', 'options'),
              [Input(reference+'my-date-picker-single', 'date')])
def update_dropbox(date):
        input_day=str(date)[5:10]
        file_name=input_day+reference+'.xlsx'
        merged_table=fx.pulling_get_performance_fig(file_name)[1]
        options=[{'label': i, 'value': i} for i in merged_table['usr']]
        return options

@app.callback(Output(reference+'rates_graph', 'figure'),
        [Input(reference+'my-date-picker-single', 'date'),Input(reference+'merged_table_list', 'value'),Input(reference+'interval-tables','n_intervals')])
def update_graph(date,value,n_intervals):
        if value:
            input_day=str(date)[5:10]
            file_name=input_day+reference+'.xlsx'
            fig=fig=fx.pulling_get_performance_fig(file_name,value)[0]
            return fig
        else:
            input_day=str(date)[5:10]
            file_name=input_day+reference+'.xlsx'
            fig=fig=fx.pulling_get_performance_fig(file_name)[0]
            return fig

@app.callback(Output(reference+'load_graph', 'figure'),
        [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables','n_intervals')])
def update_graph(date,n_intervals):
        input_day=str(date)[5:10]
        file_name=input_day+reference+'.xlsx'
        fig=fx.pulling_get_load_distribution_fig(file_name)
        return fig
        
@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-tables', 'n_intervals')])
def update_time(date,n_intervals):
    input_day=str(date)
    return fx.update_time(20,4,input_day)