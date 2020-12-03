from peewee import Model, IdentityField, TextField, FloatField, IntegerField
from playhouse.postgres_ext import ArrayField

from app.models import db


class Shops(Model):
    id = IdentityField()
    name = TextField(default="")
    address = TextField(default="")
    latitude = FloatField()
    longitude = FloatField()

    open_times = ArrayField(IntegerField, default=[])
    close_times = ArrayField(IntegerField, default=[])

    class Meta:
        database = db
        db_table = 'Shops'

# Shops.drop_table()
# Shops.create_table()
