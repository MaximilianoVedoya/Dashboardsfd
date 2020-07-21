#reads all the information form the database and stores the detail file into database.xslx
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

    out_path='archive\Pulling\database.xlsx'
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return df

#recibes the name of the shift, definitiion of shifts, date and raw data(from the function get_data()
def get_rates(shift,period,date_,data):
    from datetime import date
    import datetime
    import pandas as pd
        
    def get_users(shift,date_):
        temp=data[data['Shft']==shift]
        temp=temp.sort_values(by='pulling_date_time')
        temp=temp.set_index('pulling_date_time')
        g=temp.groupby(temp.index.floor('d'))
        my_day = pd.Timestamp(date_)
        df_slice = g.get_group(my_day)   
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
    try:
        df=built_dataframe(shift,period,date_)
        df['Name']=df.index
        df=df.fillna(0)
        df2=df.T.drop(['Name'])
        df['Rate']=df2[df2>20].mean(axis=0)
        df=df.sort_values('Rate',ascending=False)
        df['Rate'] = df['Rate'].map('{:,.2f}'.format)
        string=str(date_)[5:10]+shift+'.xlsx'
        df.to_excel('archive/Pulling/'+string)
    except:
        pass
    
#smalls function to reads the date from the users (i might not need this, maybe I can read it from the input itself)
def date_reader():
    import pandas as pd
    import pickle
    f = open('date.pckl', 'rb')
    obj = pickle.load(f)
    f.close()
    return pd.Timestamp(obj)

#it should let you know when was the last time the table was updated 
def update_time(start,finish):
    import datetime
    import time
    from apps import functions as fx
    hour=int(time.ctime()[11:13])
    today=time.ctime()[8:10]
    user_input=str(fx.date_reader())[8:10]
    if today==user_input:
        if hour>=20 or hour<=4:
            now = datetime.datetime.now()  
            return 'Last update '+now.strftime("%H:%M %m-%d")
        else:
            if hour>=start and hour<=finish:
                now = datetime.datetime.now()    
                return 'Last update '+now.strftime("%H:%M %m-%d")
            else:
                today = datetime.date.today()
                return f'Last update {finish}:00 {str(today)[5:]}'
    else:
        return f'Last update {finish}:00 {str(fx.date_reader())[5:10]}'

# file_name= day-monthMorning shift.xslx (07-15Morning shift)
# this is a auxiliar fucntions used to rearange information form the database
def main_table(file_name : str):
    import pandas as pd 
    df=pd.read_excel('archive/Pulling/'+file_name)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df=df.set_index('Name')
    df.loc['Total',:]=df.sum(axis=0)
    return df
#it gives you the resutls table (a summary of the numbers of the day)
def get_results_table(file_name: str,df): #dataframe
    import pandas as pd
    import numpy as np
    def general_indicators(file_name: str,df):
            df2=df.iloc[:-1,:-1]
            temp=df2[df2>20]
            results=pd.DataFrame(index=np.arange(len(temp.count())))
            results['Hour']=temp.count().index
            results['Headcount']=temp.count().values
            results['Exp_Rate/person']=np.where((results['Hour']=='8:00-9:00') | (results['Hour']=='9:00-10:00'),75,100)
            results['Exp_Rate']=results['Exp_Rate/person']*results['Headcount']
            expected,real=results['Exp_Rate'].sum(axis=0),df2.sum(axis=0).sum()
            return (expected,real)
    expected,net=general_indicators(file_name,df)
    results_table=pd.DataFrame(columns=['Expected Results','Net Results','Difference'],index=np.arange(1))
    results_table['Expected Results']=expected
    results_table['Net Results']=net
    results_table['Difference']=net-expected
    return results_table
#returns main and aux tables, both used in the dashborad of each shift (main is the one that is direclty displayed)
def get_main_aux(file_name):
    import pandas as pd
    def main_table(file_name : str):
            df=pd.read_excel('archive/Pulling/'+file_name)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df=df.set_index('Name')
            df.loc['Total',:]=df.sum(axis=0)
            return df
    main=main_table(file_name)
    main.insert(loc=0,column='Reference', value=main.index)
    main['Rate']['Total']=main.loc['Total'][1:-1][main.loc['Total'][1:-1]>0].mean()
    main['Rate'] = main['Rate'].map('{:,.2f}'.format)
    df=main_table(file_name)
    aux=df.T.iloc[:-1,:]
    aux=aux[aux['Total']>0]
    aux['Hour']=aux.index
    return (main,aux)
 
def summary(n_shift,m_shift,a_shift,date):
    import time 
    import pandas as pd 
    hour=int(time.ctime()[11:13])
    u_input_day=str(date)[8:10]
    today_=time.ctime()[8:10]
    
    def get_summary(sum_):
        total=pd.DataFrame(columns=['Expected Results','Net Results','Difference'], index=pd.Series(range(4)))
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

    if today_==u_input_day:
        if hour<=4:
            sum_=n_shift
            total=get_summary(sum_)
        if hour<=13:
            sum_=n_shift+m_shift
            total=get_summary(sum_)
        else:
            sum_=n_shift+m_shift+a_shift
            total=get_summary(sum_)
        return total
    else:
        sum_=n_shift+m_shift+a_shift
        total=get_summary(sum_)
        return total

#it should be ran at the beginning to ensure the rest of the things work
#it ensure the existence of the 3 previous days, and the current day. 
def initializer(finish,start,decrement=-1):
    import pandas as pd
    import datetime

    morning=[('4:00','5:00'),('5:00','6:00'),('6:00','7:00'),('7:00','8:00'),
                    ('8:00','9:00'),('9:00','10:00'),('10:00','11:00'),('11:00','12:00')]
    afternoon=[('12:00','13:00'),('13:00','14:00'),('14:00','15:00'),('15:00','16:00'),
                    ('16:00','17:00'),('17:00','18:00'),('18:00','19:00'),('19:00','20:00')]
    night=[('20:00','21:00'),('21:00','22:00'),('22:00','23:00'),('23:00','0:00'),
                    ('0:00','1:00'),('1:00','2:00'),('2:00','3:00'),('3:00','4:00')]
    
    shifts=[('Night shift',night),('Morning shift',morning),('Afternoon shift',afternoon)]
    
    today=datetime.date.today()
    try:
        for i in range(finish,start,decrement):
            for shift in shifts: 
                date_=today-datetime.timedelta(days=i)
                date_=pd.Timestamp(date_) 
                from apps import functions as fx
                data=pd.read_excel('archive/Pulling/database.xlsx')
                fx.get_rates(shift[0],shift[1],pd.Timestamp(date_),data)
    except:
        for shift in shifts:
            try:
                data=pd.read_excel('archive/Pulling/database.xlsx')
                fx.get_rates(shift[0],shift[1],pd.Timestamp(date_),data)
            except:
                yesterday=date_-datetime.timedelta(days=1)
                file_name=str(yesterday)[5:10]+shift[0]+'.xlsx'
                df=pd.read_excel('archive/Pulling/'+file_name)
                aux=pd.DataFrame(columns=df.columns,index=df.index)
                aux['Name']=df['Name']
                file_name=str(date_)[5:10]+shift[0]+'.xlsx'
                aux.to_excel('archive/Pulling'+file_name)

#reads the database for the sorting and final putaway
def putaway_get_data():
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
        select distinct pt.CNTR_NBR lpn,pt.CREATE_DATE_TIME Sort_date_time, convert(date,pt.CREATE_DATE_TIME) Sort_Date,substring(TO_LOC.LVL,1,1) Lvl,pt.USER_ID, us.USER_FIRST_NAME+','+us.USER_LAST_NAME Usr, to_loc.DSP_LOCN To_loc,

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
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end as Sort_hour,


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

            end as Shft

        from PROD_TRKG_TRAN_WMS pt 
        left outer join LOCN_HDR_WMS fr on fr.LOCN_ID = pt.FROM_LOCN
        left outer join LOCN_HDR_WMS to_loc on to_loc.LOCN_ID = pt.TO_LOCN
        join UCL_USER_WMS us on us.USER_NAME = pt.USER_ID
        where  1=1
        and ( to_loc.AISLE = 'AM' and substring(TO_LOC.LVL,2,1) = 'F' )
    """
    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           

    reference=['lpn','Sort_date_time','Sort_Date','Lvl','USER_ID','Usr','To_loc','Sort_hour','Shft']
    df=pd.DataFrame(columns=reference,index=np.arange(len(data)))
    for item in range(len(reference)):
        for row in range(len(data)):
            df[reference[item]][row]=data[row][item]

    out_path='archive\Sorting_Putaway\putaway_database.xlsx'
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return df

#returns 2 tables main and aux to be used in the views of sorting and putaway.
def putaway_table(shift,day,schedule):
    import datetime as dt
    import pandas as pd
    data=pd.read_excel('archive/Sorting_Putaway/putaway_database.xlsx')
    def putaway_rate(user,hour,day): 
        rate=len(data[(data['Usr']==user)&(data['Sort_hour']==hour)&(data['Sort_Date']==str(day)[:-9])]['lpn'].unique())
        return rate
    data=data.sort_values('Sort_date_time',ascending=False)
    users=data[(data['Sort_Date']==str(day)[:10]) & (data['Shft']==shift)]['Usr'].unique()
    df=pd.DataFrame(columns=schedule, index=users)
    for name in users:
        for hour in schedule:
            df[hour][name]= putaway_rate(name,hour,day)
    rates=df[df[df.columns]>20].mean(axis=1)
    df['Rates']=rates
    df=df.sort_values('Rates',ascending=False)
    temp=df.sum(axis=0)
    df=df.T
    df['Total']=temp
    df=df.T
    dic={name: 0 for name in df.index}
    for name in dic.keys():
        if name!='Total':
            dic[name]=data[data['Usr']==name]['Lvl'].iloc[0]
        else:
            dic[name]=0
    df.insert(0,'Current Level',dic.values())
    df['Rates']['Total']=df.loc['Total'][1:-1].mean()
    aux=df[df.columns[1:]].T
    aux['hours']=aux.index

    # pd.to_excel(archive/Sorting_Putaway/)

    return (df,aux)