import os

if os.environ["SERVICE_ENV"] == 'development':
  influx_db = {
    "host": "localhost",
    "port": 8086,
    "user": "username",
    "password": "password",
    "database": "database_name",
  }

elif os.environ["SERVICE_ENV"] == 'production':
  influx_db = {
    "host":  os.environ["INFLUX_HOST"],
    "port": os.environ["INFLUX_PORT"],
    "user": os.environ["INFLUX_USER"],
    "password": os.environ["INFLUX_PASSWORD"],
    "database": os.environ["INFLUX_DATABASE"],
  }
