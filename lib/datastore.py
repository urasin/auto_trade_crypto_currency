from influxdb import InfluxDBClient
import settings

class DataStore:
  def __init__(self, measurement):
    self.measurement = measurement
    self.client = self.getInfluxDBClient()

  def getInfluxDBClient(self):
    return InfluxDBClient(
        settings.influx_db['host'],
              settings.influx_db['port'],
              settings.influx_db['user'],
              settings.influx_db['password'],
              settings.influx_db['database'],
          )

