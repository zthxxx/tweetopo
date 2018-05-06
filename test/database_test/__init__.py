from lib.conffor import conffor
from lib.database import set_connect

CONFIG_FILE = 'test/database_test/db_unit_test.json'


def connect_mongo():
    config = conffor.load(CONFIG_FILE)
    mongo_conf = config['mongo']
    set_connect(**mongo_conf)


connect_mongo()
