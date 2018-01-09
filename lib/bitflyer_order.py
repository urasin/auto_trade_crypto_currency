import os
import time

import pybitflyer

class BitflyerOrder:
  # api doc https://lightning.bitflyer.jp/docs/playground?lang=en
  def __init__(self):
    self.api = pybitflyer.API(api_key=os.environ["API_KEY"], api_secret=os.environ["API_SECRET"])

  def buy(self):
    child_order_acceptance_id = self.execute_buy()
    if child_order_acceptance_id:
      print('Sucess Buy bitflyer!')
      # child_order_acceptance_idがdbに登録されるのをまつ
      time.sleep(5)
      return self.show_execution(child_order_acceptance_id)
    else:
      print('False Buy bitflyer!')
      return False

  def sell(self):
    child_order_acceptance_id = self.execute_sell()
    if child_order_acceptance_id:
      print('Sucess SELL bitflyer!')
      # child_order_acceptance_idがdbに登録されるのをまつ
      time.sleep(5)
      return self.show_execution(child_order_acceptance_id)
    else:
      print('False SELL bitflyer!')
      return False

  def execute_buy(self):
    params = self.get_sendchildorder_params("BUY")
    return self.api.sendchildorder(**params).get('child_order_acceptance_id')

  def execute_sell(self):
    params = self.get_sendchildorder_params("SELL")
    return self.api.sendchildorder(**params).get('child_order_acceptance_id')

  def show_execution(self, child_order_acceptance_id):
    # 返り値
    # {'child_order_acceptance_id': 'JRF20171205-120348-852407',
    #   'child_order_id': 'JOR20171205-120348-035693',
    #   'commission': 3e-06,
    #   'exec_date': '2017-12-05T12:03:48.173',
    #   'id': 82773077,
    #   'price': 1312199.0,
    #   'side': 'BUY',
    #   'size': 0.002
    # }
    # or
    # None
    params = self.get_executions_params(child_order_acceptance_id)
    results = self.api.getexecutions(**params)
    for result in results:
      return result
    return {}

  def get_sendchildorder_params(self, side):
    return {
        "product_code": "BTC_JPY",
        "child_order_type": "MARKET",
        "side": side,
        "size": 0.004,
        "time_in_force": "GTC",
    }

  def get_executions_params(self, child_order_acceptance_id):
    return {
        "product_code": "BTC_JPY",
        "count": 1,
        "before": 0,
        "after": 0,
        'child_order_acceptance_id': child_order_acceptance_id,
    }
