while True:
    import time 
    from apps import functions as fx
    try:
        fx.get_data()  
        fx.initializer_Pulling(1,-1)
        fx.putaway_get_data()
        fx.initializer_Sorting(1,-1)
        fx.shuttle_get_table()
        time.sleep(60*5)
    except:
        pass
