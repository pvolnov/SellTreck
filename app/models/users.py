from peewee import Model, IdentityField, TextField, BooleanField
from playhouse.cockroachdb import JSONField

from app.models import db


class Users(Model):
    id = IdentityField()
    name = TextField(default="")
    login = TextField(default="")
    password = TextField(default="")
    ip = TextField(default="0.0.0.0")
    notification = BooleanField(default=False)
    cart_list = JSONField(default=[])
    top_treks = JSONField(default=[])
    state = JSONField(default={})

    class Meta:
        database = db
        db_table = 'Users'

# Users.drop_table()
# Users.create_table()
