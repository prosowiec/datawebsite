import database as _database
import sqlalchemy.orm as _orm
from sqlalchemy.sql import func
#import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import StringIO
import numpy as np

import plots
import database as _database
from models import offer_table_otomoto,offer_table_autoscout

def get_db():
    db = _database.SessionLocal()
    
    try:
        yield db
    finally:
        db.close()



def get_offer_otomoto(db,brand:str,model:str, mileage_min:int ='',mileage_max:int = '',year_min:int = 0,year_max:int = '',
                   price_min:int = '', price_max:int = '',min_eng_cap:int = '',max_eng_cap:int = '' ):

    offers = db.query(offer_table_otomoto.brand,offer_table_otomoto.model,offer_table_otomoto.production_date,
    func.avg(offer_table_otomoto.price),func.avg(offer_table_otomoto.mileage),func.count(offer_table_otomoto.brand)).group_by(
    offer_table_otomoto.production_date,offer_table_otomoto.brand,offer_table_otomoto.model).filter(
    offer_table_otomoto.brand == brand,offer_table_otomoto.model == model,offer_table_otomoto.currency =='PLN').order_by(offer_table_otomoto.production_date)

    if mileage_min != '':
        offers = offers.filter(offer_table_otomoto.mileage >= mileage_min)
    if mileage_max != '':
        offers = offers.filter(offer_table_otomoto.mileage <= mileage_max)
    if year_min != '':
        offers = offers.filter(offer_table_otomoto.production_date >= year_min)
    if year_max != '':
        offers = offers.filter(offer_table_otomoto.production_date <= year_max)   
    if min_eng_cap != '':
        offers = offers.filter(offer_table_otomoto.engine_capacity >= min_eng_cap)
    if max_eng_cap != '':
        offers = offers.filter(offer_table_otomoto.engine_capacity <= max_eng_cap)  
    if price_min != '':
        offers = offers.filter(offer_table_otomoto.price >= price_min)
    if price_max != '':
        offers = offers.filter(offer_table_otomoto.price <= price_max)          

    offers = offers.all()
    offers = np.array(offers)
    x_year  = offers[:,2]
    y_avg_price = offers[:,3]
    y_avg_mileage = offers[:,4]
    volume = offers[:,5]

    y_avg_price = y_avg_price.astype(int)
    y_avg_mileage = y_avg_mileage.astype(int)


    return x_year,y_avg_price,y_avg_mileage,volume




def get_offer_autoscout24(db,brand:str,model:str, mileage_min:int ='',mileage_max:int = '',year_min:int = 0,year_max:int = '',
                   price_min:int = '', price_max:int = '',min_power:int = '',max_power:int = '' ):

    offers = db.query(offer_table_autoscout.brand,offer_table_autoscout.model,offer_table_autoscout.year,
    func.avg(offer_table_autoscout.price),func.avg(offer_table_autoscout.mileage),func.count(offer_table_autoscout.brand)).group_by(
    offer_table_autoscout.year,offer_table_autoscout.brand,offer_table_autoscout.model).filter(
    offer_table_autoscout.brand == brand,offer_table_autoscout.model == model).order_by(offer_table_autoscout.year)

    if mileage_min != '':
        offers = offers.filter(offer_table_autoscout.mileage >= mileage_min)
    if mileage_max != '':
        offers = offers.filter(offer_table_autoscout.mileage <= mileage_max)
    if year_min != '':
        offers = offers.filter(offer_table_autoscout.year >= year_min)
    if year_max != '':
        offers = offers.filter(offer_table_autoscout.year <= year_max)   
    if min_power != '':
        offers = offers.filter(offer_table_autoscout.power >= min_power)
    if max_power != '':
        offers = offers.filter(offer_table_autoscout.power <= max_power)  
    if price_min != '':
        offers = offers.filter(offer_table_autoscout.price >= price_min)
    if price_max != '':
        offers = offers.filter(offer_table_autoscout.price <= price_max)          

    offers = offers.all()
    offers = np.array(offers)
    x_year  = offers[:,2]
    y_avg_price = offers[:,3]
    y_avg_mileage = offers[:,4]
    volume = offers[:,5]

    y_avg_price = y_avg_price.astype(int)
    y_avg_mileage = y_avg_mileage.astype(int)
    volume = volume.astype(int)
    #np.multiply(y_avg_price, 4.69 )
    y_avg_price = y_avg_price * 4.69


    return x_year,y_avg_price,y_avg_mileage,volume


def charts(x_year,y_avg_price,y_avg_mileage,volume):
    
    chart1 = plots.price_bar(x_year=x_year,y_avg_price=y_avg_price)
    chart2 = plots.mileage_bar(x_year=x_year,y_avg_mileage =y_avg_mileage)
    chart3 = plots.price_and_mileage_bar(x_year=x_year,y_avg_price=y_avg_price, y_avg_mileage = y_avg_mileage)
    chart4 = plots.price_and_mileage_plot(x_year=x_year,y_avg_price=y_avg_price, y_avg_mileage = y_avg_mileage)
    chart5 = plots.volume_bar(x_year=x_year,volume =volume)

    return chart1, chart2,chart3, chart4,chart5


    

def validate_x(auto_x_year,auto_y_avg_price,auto_y_avg_mileage,auto_volume,oto_x_year,oto_y_avg_price,oto_y_avg_mileage,oto_volume):
    
    i = len(auto_x_year) -1
    while(i!=-1):
        if auto_x_year[i] not in oto_x_year:
            auto_x_year = np.delete(auto_x_year, i)
            auto_y_avg_mileage = np.delete(auto_y_avg_mileage, i)
            auto_y_avg_price = np.delete(auto_y_avg_price, i)
            auto_volume = np.delete(auto_volume, i)
        i = i-1
    

    i = len(oto_x_year) -1
    while(i!=-1):
        if oto_x_year[i] not in auto_x_year:
            oto_x_year = np.delete(oto_x_year, i)
            oto_y_avg_mileage = np.delete(oto_y_avg_mileage, i)
            oto_y_avg_price = np.delete(oto_y_avg_price, i)
            oto_volume = np.delete(oto_volume, i)
        i = i-1

    return auto_x_year,auto_y_avg_price,auto_y_avg_mileage,auto_volume,oto_x_year,oto_y_avg_price,oto_y_avg_mileage,oto_volume