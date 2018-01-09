#!/bin/bash

SAVE_DATA_PID=`ps aux | grep -v grep | grep realtime | awk '{print $2}'`
AUTO_TRADE_PID=`ps aux | grep -v grep | grep check_and | awk '{print $2}'`

execute_save_data()
{
  ./save_trade_data.sh && echo "execute ./save_trade_data.sh"
}

execute_order()
{
  ./execute_order.sh  && echo "execute ./execute_order.sh"
}

# データー保存デーモンの再起動
if [ -z "$SAVE_DATA_PID" ]; then
  execute_save_data
else
  kill -9 $SAVE_DATA_PID && echo "kill pid=${SAVE_DATA_PID}"
  execute_save_data
fi

# 注文実行プログラムの再起動
if [ -z "$AUTO_TRADE_PID" ]; then
  execute_order
else
  kill -9 $AUTO_TRADE_PID && echo "kill pid=${AUTO_TRADE_PID}"
  execute_order
fi
