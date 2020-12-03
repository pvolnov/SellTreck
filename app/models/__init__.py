import sys


sys.path.append('../')
sys.path.append('./')

from app.config import *
from playhouse.postgres_ext import *

db = PostgresqlExtDatabase(bdname, user=bduser, password=bdpassword,
                           host=bdhost, port=bdport, autoconnect=True,
                           autorollback=True)
