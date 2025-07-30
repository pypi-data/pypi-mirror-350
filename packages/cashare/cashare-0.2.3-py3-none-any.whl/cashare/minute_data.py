from cashare.common.dname import url1
import datetime
import pandas as pd
import dateutil.relativedelta
import time
from cashare.common.get_data import _retry_get
from cashare import get_token
def min_data(ca_code,type,):


    # if start_date > (datetime.date.today().strftime('%Y-%m-%d')):
    #     return "start_date大于现在时间"
    # elif start_date > end_date:
    #     return "start_date大于end_date"
    # elif end_date > (datetime.date.today().strftime('%Y-%m-%d')):
    #     end_date = datetime.date.today().strftime('%Y-%m-%d')
    # else:
    #     pass

    start_date=end_date = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    end_date=datetime.date.today().strftime('%Y-%m-%d')
    if type=="1min":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=3, y=3)
    elif type=="5min":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=8, y=7)
    elif type == "15min":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=50, y=49)
    elif type=="30min":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=24, y=22)
    elif type == "1hour":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=90, y=80)
    elif type == "4hour":
        return dan(start_date=start_date, end_date=end_date,type=type,sk_code=ca_code, token=get_token(), x=95, y=89)
    else:
        return "输入type非法,请输入1min、5min、15min、30min、1hour、4hour"

def dan(start_date,end_date,sk_code,token,x,y,type):
    if ri(start_date, end_date) <= x:
        li = hg(sk_code=sk_code, token=token, type=type, start_date=start_date, end_date=end_date)
        # print(li)

        r = _retry_get(li,timeout=100)
        # r = httpx.get(li, timeout=100)
        r = r.rename(columns={'code': 'ca_code'})
        return r
    else:

        if ri(start_date, end_date) / y > int(ri(start_date, end_date) / y):
            n = (int(ri(start_date, end_date) / y) + 1)
        else:
            n = int(ri(start_date, end_date) / y)

        list = date_huafen(sk_code=sk_code, start_date=start_date, end_date=end_date, token=token, type=type, n=n)
        # print(list)
        return url_get(list)

def hg(sk_code,start_date,end_date,token,type):
    g_url=url1+'/us/stock/ts/'+sk_code+'/'+type+'/'+start_date+'/'+end_date+'/'+token

    return g_url
def ri(start_date,end_date):
    days=(datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days
    return days

def date_huafen(sk_code,start_date,end_date,token,type,n):
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
            li = hg(sk_code, token=token, type=type, start_date=res[i], end_date=res[i+1])
            get_list.append(li)
        else:
            end=datetime.datetime.strptime(res[i+1], '%Y-%m-%d')-dateutil.relativedelta.relativedelta(days=1)
            li=hg(sk_code,token=token,type=type,start_date=res[i],end_date=end.strftime("%Y-%m-%d"))
            get_list.append(li)
    return get_list

def url_get(url_list):
    import pandas as pd
    df = pd.DataFrame(data=None)
    for item in url_list:
        r = _retry_get(item,timeout=100)
        if r.empty:
           pass
        else:
            lsss = r.sort_values(by='date')  # 进行升序排序
            df = pd.concat([df, lsss], ignore_index=True)
            # df = df.append(lsss, ignore_index=True)
            # time.sleep(0.2)
            # print(df)
    if df.empty:
        return df
    else:
        df = df.sort_values(by='date')  # 进行升序排序
        df.drop_duplicates(subset='date', keep='first', inplace=True, ignore_index=True)  # 去重
        df = df.rename(columns={'code': 'ca_code'})

        return df

if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df=ca.min_data(ca_code="AAPL",type='1hour')
    print(df)
    # df.to_csv('5555555555555555.csv')
    pass




