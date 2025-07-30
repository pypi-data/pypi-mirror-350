import httpx
from cashare.common.dname import url1
import pandas as pd
import datetime
import json
import time
import dateutil.relativedelta
from cashare.common.get_data import _retry_get
#获取单个股票市值
def mark_c_data(code,token,start_date,end_date=str(datetime.date.today().strftime('%Y-%m-%d'))):
    if start_date > (datetime.date.today().strftime('%Y-%m-%d')):
        return "start_date大于现在时间"
    elif start_date > end_date:
        return "start_date大于end_date"
    elif end_date > (datetime.date.today().strftime('%Y-%m-%d')):
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    else:
        pass

    return dan(start_date=start_date, end_date=end_date, sk_code=code, token=token, x=1000, y=1000)

    # url = url1 + '/mc/'+code+'/'+start_date+'/'+end_date+'/'+token
    # r = httpx.get(url,timeout=100)

    # df=pd.DataFrame(r.json())
    # start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    # end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    # filtered_df = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date))]
    # df_reset = filtered_df.reset_index(drop=True)
    # return df_reset


def dan(start_date,end_date,sk_code,token,x,y):
    if ri(start_date, end_date) <= x:
        li = hg(sk_code=sk_code, token=token, start_date=start_date, end_date=end_date)

        df = _retry_get(li,timeout=100)
        if df.empty:
            return df
        else:
            start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
            end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
            filtered_df = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date))]
            df_reset = filtered_df.reset_index(drop=True)
            return df_reset

    else:

        if ri(start_date, end_date) / y > int(ri(start_date, end_date) / y):
            n = (int(ri(start_date, end_date) / y) + 1)
        else:
            n = int(ri(start_date, end_date) / y)

        list = date_huafen(sk_code=sk_code, start_date=start_date, end_date=end_date, token=token,n=n)
        return url_get(list)

def hg(sk_code,start_date,end_date,token):
    # g_url=url1+'/us/stock/ts/'+sk_code+'/'+type+'/'+start_date+'/'+end_date+'/'+token

    g_url = url1 + '/mc/' + sk_code + '/' + start_date + '/' + end_date + '/' + token

    return g_url
def ri(start_date,end_date):
    days=(datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days
    return days

def date_huafen(sk_code,start_date,end_date,token,n):
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
            li = hg(sk_code, token=token, start_date=res[i], end_date=res[i+1])
            get_list.append(li)
        else:
            end=datetime.datetime.strptime(res[i+1], '%Y-%m-%d')-dateutil.relativedelta.relativedelta(days=1)
            li=hg(sk_code,token=token,start_date=res[i],end_date=end.strftime("%Y-%m-%d"))
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
            time.sleep(0.2)
            # print(df)
    if df.empty:
        return df
    else:
        df = df.sort_values(by='date')  # 进行升序排序
        df.drop_duplicates(subset='date', keep='first', inplace=True, ignore_index=True)  # 去重

        return df





if __name__ == '__main__':
    df=mark_c_data(code='0001.HK',token='you_token',start_date='2000-09-05',end_date='2024-09-09')
    print(df)
    # # pass



