import sqlalchemy as _sql
import sqlalchemy.orm as _orm


import database as _database



class offer_table_otomoto(_database.Base):
    __tablename__ = 'otomoto_data'
    brand = _sql.Column(_sql.String)
    model = _sql.Column(_sql.String)
    production_date = _sql.Column(_sql.Integer)
    price = _sql.Column(_sql.Integer, primary_key=True)
    currency = _sql.Column(_sql.String)
    mileage = _sql.Column(_sql.Integer)
    mileage_unit = _sql.Column(_sql.String)
    engine_capacity = _sql.Column(_sql.Integer)
    engine_capacity_unit = _sql.Column(_sql.String)
    fuel_type = _sql.Column(_sql.String)
    batch_date = _sql.Column(_sql.Date)


class offer_table_autoscout(_database.Base):
    __tablename__ = 'autoscout_data'
    brand = _sql.Column(_sql.String)
    model = _sql.Column(_sql.String)
    year = _sql.Column(_sql.Integer)
    price = _sql.Column(_sql.Integer, primary_key=True)
    currency = _sql.Column(_sql.String)
    mileage = _sql.Column(_sql.Integer)
    mileage_unit = _sql.Column(_sql.String)
    power = _sql.Column(_sql.Integer)
    power_unit = _sql.Column(_sql.String)
    fuel_type = _sql.Column(_sql.String)
    batch_date = _sql.Column(_sql.Date)
