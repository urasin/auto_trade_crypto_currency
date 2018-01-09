class WriteStreamData:
  def __init__(self, influxdb):
    self.measurement = influxdb.measurement
    self.client = influxdb.client

  def execute(self, line):
    self.write_stream_data(line)

  def write_stream_data(self, dict_data):
    json_body = [
      {
        "measurement": self.measurement,
        "tags": {
          "id": dict_data['id'],
          "side": dict_data['side'],
          "buy_child_order_acceptance_id": dict_data['buy_child_order_acceptance_id'],
          "sell_child_order_acceptance_id": dict_data['sell_child_order_acceptance_id'],
        },
        "time": dict_data['exec_date'],
        "fields": {
          "price": dict_data['price'],
          "size": dict_data['size'],
        }
      }
    ]
    self.client.write_points(json_body)
