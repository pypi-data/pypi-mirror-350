from cashare.common.dname import url1
import datetime
import pandas as pd
import dateutil.relativedelta
import time
from cashare.common.get_data import _retry_get
#技术指标
def ti_data(sk_code,type,token,ma,end_date=str(datetime.date.today().strftime('%Y-%m-%d')),start_date='19000101',):


    if start_date > (datetime.date.today().strftime('%Y-%m-%d')):
        return "start_date大于现在时间"
    elif start_date > end_date:
        return "start_date大于end_date"
    elif end_date > (datetime.date.today().strftime('%Y-%m-%d')):
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    else:
        pass
    if type == "daily":
        x=20000
        y=20000
    elif type=="1min":
         x=4
         y=4
    elif type=="5min":
        x=14
        y=13
    elif type == "15min":
         x=55
         y=50
    elif type=="30min":
        x=22
        y=21
    elif type == "1hour":
         x=85
         y=80
    elif type == "4hour":
        x=85
        y=80

    else:
        return "输入type非法,请输入1min、5min、15min、30min、1hour、4hour,daily"
    if ma.split("_")[1] in ['sma','ema','wma', 'dema','tema','wa','rsi','adx','sd']:

        return dan(ma=ma, start_date=start_date, end_date=end_date, type=type, sk_code=sk_code, token=token, x=x,
               y=y)
    else:
        return "输入ma非法,格式为5_ema,同时为以下一种'sma','ema','wma', 'dema','tema','wa','rsi','adx','sd'"


def dan(start_date,end_date,sk_code,token,x,y,type,ma):
    if ri(start_date, end_date) <= x:
        li = hg(sk_code=sk_code, token=token, type=type, start_date=start_date, end_date=end_date,ma=ma)
        r = _retry_get(li,timeout=100)
        r = r.sort_values(by='date')  # 进行升序排序
        r = r.reset_index(drop=True)
        r.insert(0, 'code', sk_code)

        return r
    else:

        if ri(start_date, end_date) / y > int(ri(start_date, end_date) / y):
            n = (int(ri(start_date, end_date) / y) + 1)
        else:
            n = int(ri(start_date, end_date) / y)

        list = date_huafen(sk_code=sk_code, start_date=start_date, end_date=end_date, token=token, type=type, n=n,ma=ma)
        return url_get(list,sk_code=sk_code)

def hg(sk_code,start_date,end_date,token,type,ma):
    g_url=url1+'/ti/'+sk_code+'/'+type+'/'+ma+'/'+start_date+'/'+end_date+'/'+token
    return g_url
def ri(start_date,end_date):
    days=(datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days
    return days

def date_huafen(sk_code,start_date,end_date,token,type,n,ma):
    import datetime
    # initializing dates
    test_date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    test_date2 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    # initializing N
    N = n
    temp = []
    # getting diff.
    diff = (test_date2 - test_date1) // N
    for idx in range(0, N+1):
        temp.append((test_date1 + idx * diff))

    res = []
    for sub in temp:
        res.append(sub.strftime("%Y-%m-%d"))
    get_list=[]
    for i in range(len(res)-1):
        if i ==len(res)-2:
            li = hg(sk_code, token=token, type=type, start_date=res[i], end_date=res[i+1],ma=ma)
            get_list.append(li)
        else:
            end=datetime.datetime.strptime(res[i+1], '%Y-%m-%d')-dateutil.relativedelta.relativedelta(days=1)
            li=hg(sk_code,token=token,type=type,start_date=res[i],end_date=end.strftime("%Y-%m-%d"),ma=ma)
            get_list.append(li)
    return get_list

def url_get(url_list,sk_code):
    import pandas as pd
    df = pd.DataFrame(data=None)
    for item in url_list:
        r = _retry_get(item,timeout=100)
        # print(r)
        if type(r) == str:
            print(r)
        elif r.empty:
            pass
        else:
            df = pd.concat([df, r], ignore_index=True)
            time.sleep(0.2)
    df = df.sort_values(by='date')  # 进行升序排序

    df.insert(0, 'code',sk_code )  # 插入一列
    df.drop_duplicates(subset='date', keep='first', inplace=True, ignore_index=True)  # 去重

    return df

if __name__ == '__main__':
    df=ti_data(ma='5_ema',sk_code="AAPL",token='you_token',type='1min',start_date='2023-09-21',end_date='2023-09-24')
    print(df)
    pass




