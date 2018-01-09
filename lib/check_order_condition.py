from datetime import date


class CheckOrderCondition:
  def __init__(self, influx_db):
    self.measurement = influx_db.measurement
    self.client = influx_db.client

  def can_order(self, discount_price=25000):
    # duration is minute
    now_price = self.get_now_price()
    before_price = self.get_before_price()
    print("Buy condition before_price=%s, now_price=%s,(now - before)=%s" % 
        (before_price, now_price, now_price - before_price))
    if before_price and now_price:
        return before_price - now_price >= discount_price
    else:
        return False

  def is_buy(self):
    return self.can_order()

  def is_sell(self, buy_price):
    now_price = self.get_now_price()
    print("Selling condition buy_price=%s, now_price=%s, (now - buyed)=%s" %
      (buy_price, now_price, now_price - buy_price))
    happy_condition = buy_price + 20000 <= now_price
    # sad_condition = buy_price - 2000 >= now_price
    # return happy_condition or sad_condition
    return happy_condition

  def get_before_price(self, duration=5):
    # duration is minute
    query = 'select * from %s where time > now() - %dm LIMIT 1' % (self.measurement, duration)
    result_set = self.client.query(query)
    result_list = result_set.get_points(measurement=self.measurement)
    for result in result_list:
      print("before_time=%s" % result['time'])
      return result['price']
    return False

  def get_now_price(self):
    # duration is minute
    query = 'select * from %s ORDER BY DESC LIMIT 1' % (self.measurement)
    result_set = self.client.query(query)
    result_list = result_set.get_points(measurement=self.measurement)
    for result in result_list:
      return result['price']
    return False
