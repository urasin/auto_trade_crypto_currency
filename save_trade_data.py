from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from datetime import date
import json
import os

from lib.datastore import DataStore
from lib.write_stream_data import WriteStreamData

class MySubscribeCallback(SubscribeCallback):
  def message(self, pubnub, message):
    now = date.today()
    filename = '%s_bitflyer.json' % now
    output_path = os.path.join('./log/stream', filename)

    measurement = 'bitflyer_executions_history_%s' % now.strftime('%Y_%m_%d')
    influx_db = DataStore(measurement)

    f = open(output_path,'a')
    messages_list = message.message
    for line in messages_list:
      f.write("%s\n" % json.dumps(line))
      WriteStreamData(influx_db).execute(line)
      print('%s %s' % (line['price'], line['exec_date']))

def main():
  pnconfig = PNConfiguration()
  pnconfig.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'
  pubnub = PubNub(pnconfig)
  pubnub.add_listener(MySubscribeCallback())
  pubnub.subscribe().channels('lightning_executions_BTC_JPY').execute()


if __name__ == '__main__':
  main()
