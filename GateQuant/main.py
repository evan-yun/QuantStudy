#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

'''
双均线策略: 5min & 4Hour
'''
from gateAPI import GateIO
import json
import time

# 填写 apiKey APISECRET
apiKey = 'your api key'
secretKey = 'your secret key'
# Provide constants
API_QUERY_URL = 'data.gateio.io'
API_TRADE_URL = 'api.gateio.io'
# Create a gate class instance
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)
# 设置策略池
lst_coin = ['eos_usdt']
# For回测用，设置初始资金池
initial_pool = 3000

def get_MA(coin):
    json_data = json.loads(gate_query.candle(coin, 15, 4))
    json_data['data'].reverse()
    #获取短均线值
    data_mins = [float(json_data['data'][index][-1]) for index in range(len(json_data['data'])) if index % 4 == 0 and index / 4 < 6]
    cur_short = sum(data_mins[:-1]) / float(len(data_mins) - 1)
    last_short = sum(data_mins[1:]) / float(len(data_mins) - 1)
    #获取长均线值
    data_hours = [float(json_data['data'][index][-1]) for index in range(len(json_data['data'])) if index % 240 == 0 and index / 240 < 5]
    cur_long = sum(data_hours[:-1]) / float(len(data_hours) - 1)
    last_long = sum(data_hours[1:]) / float(len(data_hours) - 1)
    log('%.6f, %.6f, %.6f, %.6f' % (cur_short, last_short, cur_long, last_long))
    return cur_short, last_short, cur_long, last_long

def check_signal(coin):
    cur_short, last_short, cur_long, last_long = get_MA(coin)
    if (cur_long - cur_short) * (last_long - last_short) < 0:
        if cur_short > cur_long:
            return 1
        else:
            return -1
    else:
        return 0

def log(content):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    filename = time.strftime('%Y%m%d', time.localtime(time.time()))
    content = timestamp + '\t' + content + '\n'
    print(content)
    with open('.\\Logs\\' + filename + '.log', 'a+') as f:
        f.write(content)

if __name__ == '__main__':
    log('开始测试...')
    log('初始资金池为 %d' % initial_pool)
    while True:
        try:
            signal = check_signal(lst_coin[0])
            if signal == 1:
                log('买入 %s' % lst_coin[0])
            elif signal == -1:
                log('卖出 %s' % lst_coin[0])
            else:
                log('本次不操作 %s' % lst_coin[0])
            time.sleep(60)
        except Exception as ex:
            log('ERROR\t' + ex.with_traceback)
            time.sleep(60)
            continue