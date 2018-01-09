import os
import traceback
import time
import random
import pytz
from datetime import datetime
from datetime import date
import dateutil.parser
from enum import Enum

from lib.datastore import DataStore
from lib.check_order_condition import CheckOrderCondition
from lib.bitflyer_order import BitflyerOrder

def main():
  state = State.no_order
  bitflyer_order = BitflyerOrder()
  while True:
    try:
      time.sleep(8)
      measurement = 'bitflyer_executions_history_%s' % date.today().strftime('%Y_%m_%d')
      influx_db = DataStore(measurement)
      check_order_condition = CheckOrderCondition(influx_db)

      filename = '%s_execute_result.log' % date.today()
      output_path = os.path.join('./log/orders', filename)

      print('state=%s' % state.name)

      # 買い注文の判定
      if state == State.no_order and check_order_condition.is_buy():
        result = bitflyer_order.buy()
        state = State.ordered
        buy_price = result.get('price')
        write_execute_log(output_path, 'buy', result)
        continue

      # 売り注文の判定
      if state == State.ordered and check_order_condition.is_sell(buy_price):
        result = bitflyer_order.sell()
        state = State.no_order
        buy_price = None
        write_execute_log(output_path, 'sell', result)
        time.sleep(300)

    except Exception:
      with open("./log/error.log", 'a') as f:
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        f.write(now.strftime('%Y-%m-%d %H:%M:%S'))
        traceback.print_exc(file=f)
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        traceback.print_exc()

class State(Enum):
  no_order = 'no_order'
  ordered = 'orderd'

def exec_date_from(result):
  if result:
    exec_date = dateutil.parser.parse(
      str(result.get('exec_date'))).astimezone(pytz.timezone('Asia/Tokyo'))
  else:
    exec_date = datetime.now(pytz.timezone('Asia/Tokyo'))
  return exec_date

def write_execute_log(output_path, action, result):
  f = open(output_path, 'a')
  line = "%s, %s, %s, %s, %s\n" % (
    action,
    result.get('price'),
    result.get('size'),
    result.get('commission'),
    exec_date_from(result).strftime('%Y-%m-%d %H:%M:%S')
  )
  f.write(line)
  f.close()


if __name__ == '__main__':
  main()
