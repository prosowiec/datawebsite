import fastapi as _fastapi
import sqlalchemy.orm as _orm
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Form

from brand_models import brand_models_oto, brand_models_auto
from models import offer_table_otomoto
import plots
import services as _services

app = _fastapi.FastAPI()

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    global db
    db = _services._database.SessionLocal()
    try:
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


@app.post("/submit_otomoto")
async def submit_otomoto(request: _fastapi.Request):

    form_data = await request.form()
    brand_model = form_data['brand_model']
    year_min = form_data['year_min']
    year_max = form_data['year_max']
    mileage_min = form_data['mileage_min']
    mileage_max = form_data['mileage_max']
    min_eng_cap = form_data['min_eng_cap']
    max_eng_cap = form_data['max_eng_cap']
    price_min = form_data['price_min']
    price_max = form_data['price_max']
    
    if brand_model == '':
        return 'Enter brand and model!!!'

    brand , model = brand_model.split(' ', 1)
    

    try:
        x_year,y_avg_price,y_avg_mileage,volume = _services.get_offer_otomoto(db = db,brand=brand,model=model,mileage_min=mileage_min,mileage_max=mileage_max
        ,year_min=year_min, year_max= year_max, price_max= price_max,price_min=price_min, min_eng_cap=min_eng_cap, max_eng_cap=max_eng_cap)

        chart1, chart2, chart4,chart5 = _services.charts(x_year,y_avg_price,y_avg_mileage,volume)
        
        return chart1 + ' <br><br> ' + chart5 +' <br><br>' +  chart2 + ' <br><br>' + chart4+ ' <br><br>'
    except IndexError:
        return '<div class="ui warning message"><i class="close icon"></i><div class="header">Result not found</div>Change filter settings</div>'
    

@app.post("/submit_autoscout24")
async def submit_autoscout24(request: _fastapi.Request):
    form_data = await request.form()
    brand_model = form_data['brand_model']
    year_min = form_data['year_min']
    year_max = form_data['year_max']
    mileage_min = form_data['mileage_min']
    mileage_max = form_data['mileage_max']
    min_power = form_data['min_power']
    max_power = form_data['max_power']
    price_min = form_data['price_min']
    price_max = form_data['price_max']
    
    if brand_model == '':
        return '<div class="ui header">Enter brand and model!!!</div>'

    brand , model = brand_model.split(' ', 1)

    try:
        x_year,y_avg_price,y_avg_mileage,volume = _services.get_offer_autoscout24(db = db,brand=brand,model=model,mileage_min=mileage_min,mileage_max=mileage_max
        ,year_min=year_min, year_max= year_max, price_max= price_max,price_min=price_min, min_power=min_power, max_power=max_power)
        
        chart1, chart2, chart4,chart5 = _services.charts(x_year,y_avg_price,y_avg_mileage,volume)
        return chart1 + ' <br><br> ' + chart5 +' <br><br>' +  chart2 + ' <br><br>' + chart4+ ' <br><br>'
    except IndexError:
        return '<div class="ui warning message"><i class="close icon"></i><div class="header">Result not found</div>Change filter settings</div>'


@app.post("/compare_both")
async def get_compare_both(request: _fastapi.Request):

    form_data = await request.form()
    brand_model_oto = form_data['brand_model_oto']
    oto_year_min = form_data['oto_year_min']
    oto_year_max = form_data['oto_year_max']
    oto_mileage_min = form_data['oto_mileage_min']
    oto_mileage_max = form_data['oto_mileage_max']
    oto_min_eng_cap = form_data['oto_min_eng_cap']
    oto_max_eng_cap = form_data['oto_max_eng_cap']
    oto_price_min = form_data['oto_price_min']
    oto_price_max = form_data['oto_price_max']

    brand_model_auto = form_data['brand_model_auto']
    auto_year_min = form_data['auto_year_min']
    auto_year_max = form_data['auto_year_max']
    auto_mileage_min = form_data['auto_mileage_min']
    auto_mileage_max = form_data['auto_mileage_max']
    auto_min_power = form_data['auto_min_power']
    auto_max_power = form_data['auto_max_power']
    auto_price_min = form_data['auto_price_min']
    auto_price_max = form_data['auto_price_max']

    oto_brand , oto_model = brand_model_oto.split(' ', 1)
    auto_brand , auto_model = brand_model_auto.split(' ', 1)

    try:
        auto_x_year,auto_y_avg_price,auto_y_avg_mileage,auto_volume = _services.get_offer_autoscout24(db = db,brand=auto_brand,model=auto_model,
        mileage_min=auto_mileage_min,mileage_max=auto_mileage_max,year_min=auto_year_min, year_max= auto_year_max, price_max= auto_price_max,
        price_min=auto_price_min, min_power=auto_min_power, max_power=auto_max_power)

        oto_x_year,oto_y_avg_price,oto_y_avg_mileage,oto_volume = _services.get_offer_otomoto(db = db,brand=oto_brand,model=oto_model,
        mileage_min=oto_mileage_min,mileage_max=oto_mileage_max,year_min=oto_year_min, year_max= oto_year_max, price_max= oto_price_max,
        price_min=oto_price_min, min_eng_cap=oto_min_eng_cap, max_eng_cap=oto_max_eng_cap)

        
        auto_x_year,auto_y_avg_price,auto_y_avg_mileage,auto_volume,oto_x_year,oto_y_avg_price,oto_y_avg_mileage,oto_volume = _services.validate_x(
            auto_x_year,auto_y_avg_price,auto_y_avg_mileage,auto_volume,oto_x_year,oto_y_avg_price,oto_y_avg_mileage,oto_volume
        )
        chart , chart2 = _services.charts_compare(oto_x_year,auto_x_year,oto_y_avg_price,auto_y_avg_price,oto_y_avg_mileage,auto_y_avg_mileage)

        return chart + chart2

    except IndexError:
        return '<div class="ui warning message"><i class="close icon"></i><div class="header">Result not found</div>Change filter settings</div>'







@app.get("/")
async def index(request: _fastapi.Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/otomoto")
async def index(request: _fastapi.Request):
    return templates.TemplateResponse("otomoto.html", {"request": request, "brand_models":brand_models_oto})

@app.get("/autoscout24")
async def index(request: _fastapi.Request):
    return templates.TemplateResponse("autoscout24.html", {"request": request, "brand_models":brand_models_auto})


@app.get("/compare_both")
async def index(request: _fastapi.Request):
    return templates.TemplateResponse("compare_both.html", {"request": request, 
    "brand_models_auto":brand_models_auto, "brand_models_oto":brand_models_oto,})











