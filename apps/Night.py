from datetime import date
import pandas as pd
import numpy as np 
from app import app

#definition of shifts 
morning=[('4:00','5:00'),('5:00','6:00'),('6:00','7:00'),('7:00','8:00'),
                ('8:00','9:00'),('9:00','10:00'),('10:00','11:00'),('11:00','12:00')]
afternoon=[('12:00','13:00'),('13:00','14:00'),('14:00','15:00'),('15:00','16:00'),
                ('16:00','17:00'),('17:00','18:00'),('18:00','19:00'),('19:00','20:00')]
night=[('20:00','21:00'),('21:00','22:00'),('22:00','23:00'),('23:00','0:00'),
                ('0:00','1:00'),('1:00','2:00'),('2:00','3:00'),('3:00','4:00')]
def get_data():
    import pandas as pd
    import numpy as np
    from datetime import date
    import pyodbc

    connection = pyodbc.connect('DRIVER={SQL Server};'

                                'SERVER=nj01prdbidb01.intranet.biz.freshdirect.com;'

                                'DATABASE=DASHBOARD;'

                                'UID=DASH_READONLY;'

                                'PWD=Mbers0nyon#123;'
                                
                                "autocommit = True")
    query="""
        Select 
        distinct
        pt.USER_ID as User_id,
        concat(us.USER_FIRST_NAME,',',us.USER_LAST_NAME) usr,
        pt.task_id,
        pt.CNTR_NBR ilpn,
        case when isNull(td.STAT_CODE,td2.STAT_CODE) = 40 then 'Pulled' 
        when isNull(td.STAT_CODE,td2.STAT_CODE) = 99 then 'Pulled then Ctrl-G'
        else 'Complete' end as status,
        concat(lh0.WORK_AREA,'/',lh0.WORK_GRP) 'WA/WG',
        pt.CREATE_DATE_TIME pulling_date_time,
        lh0.dsp_locn Pull_location,
        convert(date,pt.CREATE_DATE_TIME) pulling_date,

        case when th.INVN_NEED_TYPE = 1 then 'INT1' 
        when th.INVN_NEED_TYPE = 2 then 'INT2' 
        when th.INVN_NEED_TYPE = 90 then 'INT90' 
        end as INT_task,

        CASE
            WHEN Th.Task_Type = '11' THEN 'Chill Pallet'
            WHEN Th.Task_Type = '12' THEN 'Freezer Pallet Replen'
            WHEN Th.Task_Type = '13' THEN 'BTO Pallet Replen'
            WHEN Th.Task_Type = '14' THEN 'Kitchen Pallet Replen'
            WHEN Th.Task_Type = '15' THEN 'Ambient Pallet Replen'
            WHEN Th.Task_Type = '70' and  Th.START_CURR_WORK_AREA NOT like 'N%' 
                                THEN 'Ambient Case Replen'
            WHEN Th.Task_Type = '71' and Th.START_CURR_WORK_AREA NOT like 'B%' and Th.START_CURR_WORK_AREA NOT like 'N%'
                                    THEN 'Chill Case Replen' 
            WHEN Th.Task_Type = '72' THEN 'Freezer Case Replen'
            WHEN Th.Task_Type = '73' THEN 'BTO Case Replen'
            WHEN Th.Task_Type = '74' THEN 'Kitchen Case Replen'
            WHEN Th.Task_Type = '75' THEN 'Shuttle Case Replen'
            WHEN Th.Task_Type = '70' and  Th.START_CURR_WORK_AREA like 'N%' 
                                        THEN 'Supplies'
            WHEN Th.Task_Type = '71' and (Th.START_CURR_WORK_AREA like 'B%' or Th.START_CURR_WORK_AREA like 'P%')
                                    THEN 'Supplies'
            WHEN Th.Task_Type = '76' THEN 'Chill MTS Replen'
            WHEN Th.Task_Type in ('40','41') THEN 'Pick from reserve INT2'
            WHEN Th.Task_Type = '50' THEN 'Recall INT90'
        END AS "Task description",

        --concat(td.task_id,td.CNTR_NBR) id,

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end as Pull_hour,


        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then 'Morning shift'

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then 'Afternoon shift'

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM','12AM','01AM','02AM','03AM') then 'Night shift'

            end as Shft,

        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then convert(date,pt.CREATE_DATE_TIME)

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then convert(date,pt.CREATE_DATE_TIME+1)

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM') then convert(date,pt.CREATE_DATE_TIME+1)

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12AM','01AM','02AM','03AM') then convert(date,pt.CREATE_DATE_TIME)

            end as Delivery
                        
        from PROD_TRKG_TRAN_WMS pt

        left outer join (select distinct th.task_id,th.Task_type,th.INVN_NEED_TYPE,Th.START_CURR_WORK_AREA from TASK_HDR_WMS th where th.INVN_NEED_TYPE in (1,2,90)
        and th.CREATE_DATE_TIME > cast(getdate()-6 as date)
        )th
        on th.TASK_ID = pt.TASK_ID

        left outer join (select distinct pt.CNTR_NBR,pt.task_id,concat(pt.from_locn,pt.CNTR_NBR)id,pt.CREATE_DATE_TIME from PROD_TRKG_TRAN_WMS pt
        inner join (
        select  distinct min(pt.CREATE_DATE_TIME)CREATE_DATE_TIME,concat(pt.from_locn,pt.CNTR_NBR)id from PROD_TRKG_TRAN_WMS pt where
        convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-5 as date) 
        and pt.TRAN_TYPE = 300 and pt.TRAN_CODE = '005' and pt.TASK_ID is not null
        group by concat(pt.from_locn,pt.CNTR_NBR)
        )ptn on ptn.id = concat(pt.FROM_LOCN,pt.cntr_nbr) and ptn.CREATE_DATE_TIME = pt.CREATE_DATE_TIME
        where convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-5 as date) and pt.TRAN_TYPE = 300 and pt.TASK_ID is not null 
        and pt.TRAN_CODE = '005'
        )ptn
        on ptn.id = concat(pt.FROM_LOCN,pt.cntr_nbr)
        and ptn.CREATE_DATE_TIME > pt.CREATE_DATE_TIME

        left outer join (select CONCAT(td.task_id,td.CNTR_NBR)id, td.TASK_ID, td.STAT_CODE from TASK_DTL_WMS td where td.MOD_DATE_TIME > cast(getdate()-6 as date))td
        on td.id = concat(ptn.TASK_ID,ptn.cntr_nbr)

        left outer join (select CONCAT(td.task_id,td.CNTR_NBR)id, td.TASK_ID, td.STAT_CODE from TASK_DTL_WMS td where td.MOD_DATE_TIME > cast(getdate()-6 as date))td2
        on td2.id = concat(pt.TASK_ID,pt.cntr_nbr)

        left outer join LOCN_HDR_WMS lh0
        on lh0.LOCN_ID = pt.FROM_LOCN

        left outer join ITEM_MASTER_WMS im
        on im.ITEM_ID = pt.ITEM_ID


        left outer join ucl_user_wms us
        on us.USER_NAME = pt.USER_ID

        where 
        convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-6 as date)
        and pt.TRAN_TYPE = 300 and pt.TRAN_CODE = '006' and pt.TASK_ID is not null
        and th.Task_type not in (00,01,02,03,04,05,06,07,08)
        and (lh0.ZONE in ('A1','A2','A3','A4','A5','A6','A7'))
    """

    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           

    reference=['User_id','usr','task_id','ilpn','status','WA/WG','pulling_date_time','Pull_location','pulling_date','INT_task','Task description','Pull_hour','Shft','Delivery']
    df=pd.DataFrame(columns=reference,index=np.arange(len(data)))
    for item in range(len(reference)):
        for row in range(len(data)):
            df[reference[item]][row]=data[row][item]    
    return df
def get_rates(shift,period,date_):
    #pull the data from the database
    data=get_data()

    from datetime import date
    import pandas as pd
    
    def get_users(shift,date_):
            temp=data[data['Shft']==shift]
            temp=temp.sort_values(by='pulling_date_time')
            temp=temp.set_index('pulling_date_time')
            g=temp.groupby(temp.index.floor('d'))
            my_day = pd.Timestamp(date_)
            df_slice = g.get_group(date_)   
            return list(df_slice.usr.unique())

    def get_list(start,finish,shift,date_):
            morning=data[data['Shft']==shift]
            morning=morning.sort_values(by='pulling_date_time')
            morning=morning.set_index('pulling_date_time')
            g=morning.groupby(morning.index.floor('d'))
            my_day = pd.Timestamp(date_)
            df_slice = g.get_group(my_day)      
            first_hour=df_slice.between_time(start,finish)
            operators=first_hour['usr'].unique()
            dic={employee: first_hour[first_hour['usr']==employee]['ilpn'].size for employee in operators}
            return dic

    def built_dataframe(shift,period,date_):
            list_=[s+'-'+e for s,e in period]
            list_.insert(0,'Name')
            users=get_users(shift,date_)
            df=pd.DataFrame(columns=list_, index=pd.Series(users))
            starting=[s for s,e in period]
            ending=[e for s,e in period]
            def dataframe(s,e,shift):
                for name,rate in get_list(s,e,shift,date_).items():
                    df[s+'-'+e][name]=rate
            for s,e in period:
                dataframe(s,e,shift)
            return df 

    df=built_dataframe(shift,period,date_)
    df['Name']=df.index
    df=df.fillna(0)
    df2=df.T.drop(['Name'])
    df['Rate']=df2[df2>20].mean(axis=0)
    df=df.sort_values('Rate',ascending=False)
    df['Rate'] = df['Rate'].map('{:,.2f}'.format)
    df.to_excel(shift+'.xlsx')


reference='Night shift'       

def main_table(shift=reference+'.xlsx'):
        df=pd.read_excel(shift)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df=df.set_index('Name')
        df.loc['Total',:]=df.sum(axis=0)
        return df
def general_indicators():
        df=main_table()
        df2=df.iloc[:-1,:-1]
        temp=df2[df2>20]
        results=pd.DataFrame(index=np.arange(len(temp.count())))
        results['Hour']=temp.count().index
        results['Headcount']=temp.count().values
        results['Exp_Rate/person']=np.where((results['Hour']=='8:00-9:00') | (results['Hour']=='9:00-10:00'),75,100)
        results['Exp_Rate']=results['Exp_Rate/person']*results['Headcount']
        expected,real=results['Exp_Rate'].sum(axis=0),df2.sum(axis=0).sum()
        return (expected,real)
    
   

m_results_table=pd.DataFrame(columns=['Expected_Results','Net Results','Difference'],index=np.arange(1))
m_results_table['Expected_Results']=general_indicators()[0]
m_results_table['Net Results']=general_indicators()[1]
m_results_table['Difference']=general_indicators()[1]-general_indicators()[0]
  
#this is only to show the table and the averga part of the graph
m_main=main_table()
m_main.insert(loc=0,column='Reference', value=m_main.index)
m_main['Rate']['Total']=m_main.loc['Total'][1:-1][m_main.loc['Total'][1:-1]>0].mean()
m_main['Rate'] = m_main['Rate'].map('{:,.2f}'.format)
        
#Developing app
import dash
import dash_table
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#app = dash.Dash(__name__)
df=main_table()
df2=df.T.iloc[:-1,:]
df2=df2[df2['Total']>0]
df2['Hour']=df2.index
fig=px.line(df2, x='Hour', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=df2.index, y=[float(m_main['Rate'].loc['Total']) for i in df2.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(float(m_main['Rate'].loc['Total']))))
def time():
    import datetime
    now = datetime.datetime.now()    
    return 'Last update '+now.strftime("%H:%M %d/%m")
now=time()

layout =html.Div(
    [
        html.H1('Pulling Ambient '+reference,style={'float': 'center'}),
        html.H2(id=reference+'time_update',children=''),
        html.Div([dash_table.DataTable(
                                        id=reference+'main_table',
                                        columns=[{"name": i, "id": i} for i in m_main.columns],
                                        data=m_main.to_dict('records'),
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
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 75'.format(x)},
                                                    'background_color': '#B3E577',
                                                } for x in df.columns

                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 35 && {{{0}}} <75'.format(x)},
                                                    'background_color': '#E0ED4B',
                                                } for x in df.columns
                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 35'.format(x)},
                                                    'background_color': '#F78B54',
                                                } for x in df.columns
                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                    'background_color': '#fafcfa',
                                                } for x in df.columns
                                            ]
                                            +
                                            
                                            [
                                                {
                                                    'if': {'column_id': 'Rate'},'fontWeight': 'bold',
                                                } 
                                            ]
                                        ),
                dash_table.DataTable(   id='results_table',
                                        columns=[{"name": i, "id": i} for i in m_results_table.columns],
                                        data=m_results_table.to_dict('records'),
                                        style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'}
                                        )
                    ],style={'width':'70%'}),
        html.Div(dcc.Dropdown(
                    id=reference+'name_list',
                    options=[{'label': i, 'value': i} for i in df.index],
                    value='Pull_Rates',
                    placeholder='Select Operator',
                    searchable=False,
                    multi=False
                ),style={'width': '28%', 'float': 'center', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id=reference+'rates_graph',figure=fig,style={'width': '65%'})),
        html.Div(dcc.Interval(
            id=reference+'interval-main_table',
            interval=3*60*1000, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval-results_table',
            interval=3*60*1000, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval_graph',
            interval=3*60*1000, # in milliseconds
            n_intervals=0)),
    ])

@app.callback(
        Output(reference+'rates_graph', 'figure'),
        [Input(reference+'name_list', 'value'),Input(reference+'interval_graph', 'n_intervals')])

def update_graph(name_list,interval_graph):
        if name_list!='Pull_Rates' and name_list!='Total' and name_list:
            df=main_table()
            dff=df.T.iloc[:-1,:]
            dff=dff[dff['Total']>0]
            dff['Hour']=dff.index
            fig=px.line(dff, x='Hour', y=name_list, title=name_list+' Performance curve')
            fig.add_trace(go.Scatter(x=dff.index, y=[df['Rate'].loc[name_list] for i in dff.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(df['Rate'].loc[name_list])))
            return fig
        else :
            df=main_table()
            dff=df.T.iloc[:-1,:]
            dff=dff[dff['Total']>0]
            dff['Hour']=dff.index
            fig=px.line(dff, x='Hour', y='Total', title='Total Performance curve')
            main=main_table()
            main.insert(loc=0,column='Reference', value=main.index)
            main['Rate']['Total']=main.loc['Total'][1:-1][main.loc['Total'][1:-1]>0].mean()
            main['Rate'] = main['Rate'].map('{:,.2f}'.format)
            fig.add_trace(go.Scatter(x=dff.index, y=[float(main['Rate'].loc['Total']) for i in dff.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(float(main['Rate'].loc['Total']))))
            return fig
   
@app.callback(Output(reference+'main_table', 'data'),
              [Input(reference+'interval-main_table', reference+'n_intervals')])
    
def update_main_table(n_intervals):
        # get_rates(reference,night,date.today())
        dff=main_table()
        dff.insert(loc=0,column='Reference', value=dff.index)
        dff['Rate']['Total']=dff.loc['Total'][1:-1][dff.loc['Total'][1:-1]>0].mean()
        dff['Rate'] = dff['Rate'].map('{:,.2f}'.format)
        dff.fillna(0)
        data=dff.to_dict('records')
        return data

@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_time(n_intervals):
        return time()

@app.callback(Output(reference+'results_table', 'data'),
              [Input(reference+'interval-results_table', reference+'n_intervals')])
    
def update_results_table(n_intervals):
        results_table['Expected_Results']=general_indicators()[0]
        results_table['Net Results']=general_indicators()[1]
        results_table['Difference']=general_indicators()[1]-general_indicators()[0]
        data=results_table.to_dict('records')
        return data

