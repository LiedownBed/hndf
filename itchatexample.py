# -*-coding=utf-8-*-

import smtplib, time,os,datetime
import tushare as ts
from pandas import Series
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itchat



def push_wechat(name, real_price, real_percent, type):
    age=10
    name=u'wwwei'
    itchat.auto_login(hotReload=True)
    account=itchat.get_friends(name)
    for i in account:
        if i[u'PYQuanPin']==name:
            toName=i['UserName']
    content=name+' ' + str(real_price)+' '+ str(real_percent)+' percent '+ type
    itchat.send(content,toUserName=toName)


def read_stock(name):
    f = open(name)
    stock_list = []

    for s in f.readlines():
        s = s.strip()
        row = s.split(';')
        # print row
        # print "code :",row[0]
        # rint "price :",row[1]
        stock_list.append(row)

    return stock_list


def meet_price(code, price_up, price_down,type):
    try:
        df = ts.get_realtime_quotes(code)
    except Exception, e:
        print e
        time.sleep(5)
        return 0
    real_price = df['price'].values[0]
    name = df['name'].values[0]
    real_price = float(real_price)
    pre_close = float(df['pre_close'].values[0])
    percent = (real_price - pre_close) / pre_close * 100
    # print percent
    # percent=df['']
    # print type(real_price)
    if real_price >= price_up:
        print '%s price higher than %.2f , %.2f' % (name, real_price, percent),
        print '%'
        push_wechat(name, real_price, percent, 'up')
    if real_price <= price_down:
        print '%s price lower than %.2f , %.2f' % (name, real_price, percent),
        print '%'
        push_wechat(name, real_price, percent, 'down')

def meet_percent(code, percent_up, percent_down,type):
    try:
        df = ts.get_realtime_quotes(code)
    except Exception, e:
        print e
        time.sleep(5)
        return 0
    real_price = df['price'].values[0]
    name = df['name'].values[0]
    real_price = float(real_price)
    pre_close = float(df['pre_close'].values[0])
    real_percent = (real_price - pre_close) / pre_close * 100
    # print percent
    # percent=df['']
    # print type(real_price)
    if real_percent >= percent_up:
        print '%s percent higher than %.2f , %.2f' % (name, real_percent, real_price),
        push_wechat(name, real_price, real_percent, 'down')
        return 1
    if real_percent <= percent_down:
        print '%s percent lower than %.2f , %.2f' % (name, real_percent, real_price),
        print '%'
        push_wechat(name, real_price, real_percent, 'down')
        return 1
# 推送一般的实盘消息
def general_info():
    t_all = ts.get_today_all()
    result = []
    t1 = t_all[t_all['changepercent'] <= -9.0].count()['changepercent']
    result.append(t1)
    for i in range(-9, 9, 1):
        temp = t_all[(i * 1.00 < t_all['changepercent']) & (t_all['changepercent'] <= (i + 1) * 1.00)].count()[
            'changepercent']
        result.append(temp)
    t2 = t_all[t_all['changepercent'] > 9.0].count()['changepercent']
    result.append(t2)
    return result



def main():
    # read_stock()
    choice = input("Input your choice:\n")

    if str(choice) == '1':
        # using price:
        stock_lists_price = read_stock('price.txt')
        while 1:
            t = 0
            for each_stock in stock_lists_price:
                code = each_stock[0]
                price_down = float(each_stock[1])
                price_up = float(each_stock[2])
                t = meet_price(code, price_up, price_down)
                if t:
                    stock_lists_price.remove(each_stock)

    if str(choice) == '2':
        # using percent
        stock_lists_percent = read_stock('percent.txt')
        while 1:
            t = 0
            for each_stock in stock_lists_percent:
                code = each_stock[0]
                percent_down = float(each_stock[1])
                percent_up = float(each_stock[2])
                t = meet_percent(code, percent_up, percent_down,type)
                if t:
                    stock_lists_percent.remove(each_stock)


if __name__ == '__main__':
    path=os.path.join(os.getcwd(),'data')
    if os.path.exists(path)==False:
        os.mkdir(path)
    os.chdir(path)

    main()
    # general_info()
    #visual()
    #monitor_break()
