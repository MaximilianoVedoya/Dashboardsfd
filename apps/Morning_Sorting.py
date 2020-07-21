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


#shifts definition
day=datetime.datetime(2020,7,20)
schedule=['04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM','12AM']

#reference is used infront of every single id of each one of the elements of the layout, to avoid duplicate callbacks
reference='Sorting Morning shift'
#refreshing time establishes the amount of time by each callback
refreshing_time=1*60*1000 #millisecods


input_day=str(fx.date_reader())
data=pd.read_excel('archive/Sorting_Putaway/putaway_database.xlsx')
main,aux=fx.putaway_table(reference[8:],input_day,schedule)

fig=px.line(aux, x='hours', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=aux.index[1:], y=[float(main['Rates'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rates'].loc['Total']))))
 

layout =html.Div(
    [   html.H1('Sorting and Putaway Ambient '+reference,style={'float': 'center'}),
        html.H2(id=reference+'time_update',children=''),
        html.Div([dash_table.DataTable( id=reference+'main',
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
                                        ),
                # dash_table.DataTable(   id=reference+'results_table',
                #                         columns=[{"name": i, "id": i} for i in results_table.columns],
                #                         data=results_table.to_dict('records'),
                #                         style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'}
                #                         )
                    ],style={'width':'70%'}),
        html.Div(dcc.Dropdown(id=reference+'name_list',
                            options=[{'label': i, 'value': i} for i in main.index],
                            value='Sort_Rates',
                            placeholder='Select Operator',
                            searchable=False,
                            multi=False),style={'width': '28%', 'float': 'center', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id=reference+'rates_graph',figure=fig,style={'width': '65%'})),
        html.Div(dcc.Interval(
            id=reference+'interval-main_table',
            interval=refreshing_time, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval-results_table',
            interval=refreshing_time, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval_graph',
            interval=refreshing_time, # in milliseconds
            n_intervals=0)),
                ])


@app.callback(
        Output(reference+'rates_graph', 'figure'),
        [Input(reference+'name_list', 'value'),Input(reference+'interval_graph', 'n_intervals')])

def update_graph(name_list,interval_graph):
        input_day=str(fx.date_reader())
        data=pd.read_excel('archive/putaway_database.xlsx')
        main,aux=fx.putaway_table(reference[8:],input_day,schedule)

        if name_list!='Sort_Rates' and name_list!='Total' and name_list:
            fig=px.line(aux, x='hours', y=name_list, title=name_list+' Performance curve')
            fig.add_trace(go.Scatter(x=aux.index[1:], y=[float(main['Rates'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rates'].loc['Total']))))
            return fig
        else :
            fig=px.line(aux[1:], x='hours', y='Total', title='Total Performance curve')
            fig.add_trace(go.Scatter(x=aux.index[1:], y=[float(main['Rates'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rates'].loc['Total']))))
            return fig
        print(main,aux)
   
@app.callback(Output(reference+'main_table', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals')])
    
def update_main_table(n_intervals):
        input_day=str(fx.date_reader())[5:10]
        data=pd.read_excel('archive/putaway_database.xlsx')
        main,aux=fx.putaway_table(reference[8:],input_day,schedule)
        data=main.to_dict('records')
        return data

@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_time(n_intervals):
        return fx.update_time(4,12)

# @app.callback(Output(reference+'results_table', 'data'),
#               [Input(reference+'interval-results_table', 'n_intervals')])
# def update_results_table(n_intervals):
#     file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
#     df=fx.main_table(file_name)
#     results_table=fx.get_results_table(file_name,df)
#     data=results_table.to_dict('records')
#     return data




