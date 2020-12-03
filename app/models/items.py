from peewee import Model, IdentityField, TextField, FloatField
from playhouse.cockroachdb import JSONField
from playhouse.postgres_ext import ArrayField, BigIntegerField

from app.models import db


class Items(Model):
    id = IdentityField()
    hash = BigIntegerField(null=False,unique=True)
    shop = TextField()
    price = FloatField()
    discount = FloatField()
    params = FloatField()
    nice = FloatField()

    name = TextField(default="")
    main_name = TextField(default="")
    short_name = TextField(default="")
    img = TextField(null=True)
    url = TextField(null=True)

    keywords = ArrayField(TextField)
    local_dictionary = JSONField(default={})

    class Meta:
        database = db
        db_table = 'Items'


# Items.drop_table()
# Items.create_table()
