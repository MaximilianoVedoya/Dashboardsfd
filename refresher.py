while True:
    import time 
    from apps import functions as fx
    try:
        # fx.get_data()  
        fx.pulling_initializer(1,-1)
        # fx.sorting_get_data()
        fx.initializer_Sorting(1,-1)
        # fx.shuttle_get_table()
        # fx.fill_get_data()
        fx.fill_initializer(1,-1)
        time.sleep(60*5)
    except:
        pass
