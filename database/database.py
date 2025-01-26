from config_data.config import config

if config.type_db == 'sqllite':
    from database.database_sqllite import *
elif config.type_db == 'mysql':
    from database.database_mysql import *