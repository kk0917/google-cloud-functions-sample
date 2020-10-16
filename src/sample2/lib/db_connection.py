import os

import sqlalchemy
from sqlalchemy import create_engine

# Set the following variables depending on your specific
# connection name and root password from the earlier steps:
CONNECTION_NAME  = os.environ["CLOUD_SQL_CONNECTION_NAME"]
DB_USER          = os.environ['DB_USER']
DB_USER_PASSWORD = os.environ['DB_USER_PASSWORD']
DB_NAME          = os.environ['DB_NAME']
DRIVER_NAME      = 'postgres+pg8000'
query_string     = dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(CONNECTION_NAME)})

engine = create_engine(
    sqlalchemy.engine.url.URL(
        drivername=DRIVER_NAME,
        username=DB_USER,
        password=DB_USER_PASSWORD,
        database=DB_NAME,
        query=query_string,
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800)

def insert(params, identified_name):
    return connect('INSERT', params, identified_name)

def select(params):
    return connect('SELECT', params)

def connect(type, params, _identified_name=None):
    try:
        with engine.connect() as conn:
            result = None

            if type == 'INSERT':
                trans  = conn.begin()
                # TODO: Write the query in hard code as a provisional response
                result = conn.execute("INSERT INTO master.m_company (sys_id, sys_master_id, unique_name) VALUES ({}, {}, '{}')".format(params['sys_id'], params['sys_master_id'], _identified_name))
                trans.commit()
            elif type == 'SELECT':
                # TODO: Write the query in hard code as a provisional response
                result = conn.execute("SELECT * FROM master.m_company WHERE sys_id = {} AND sys_master_id = {} AND is_deleted = false".format(params['sys_id'], params['sys_master_id']))

            conn.close()

            return result

    except Exception as e:
        return 'Error: {}'.format(str(e))
