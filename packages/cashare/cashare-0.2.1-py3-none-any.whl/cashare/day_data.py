from cashare.common.dname import url1
import datetime
import pandas as pd
import dateutil.relativedelta
import time
from cashare.common.get_data import _retry_get
from cashare.common.var_date import check_date

def daily_data(sk_code,token,end_date=str(datetime.date.today().strftime('%Y%m%d')),start_date='19000101',x=5000, y=5000):

    ls=check_date(start_date=start_date,end_date=end_date)
    if isinstance(ls, str):
        return ls
    else:
        start_date=ls[0]
        end_date=ls[1]
    if ri(start_date, end_date) <= x:
        li = hg(sk_code=sk_code, token=token, start_date=start_date, end_date=end_date)
        r =  _retry_get(li,timeout=100)
        return r
    else:
        if ri(start_date, end_date) / y > int(ri(start_date, end_date) / y):
            n = (int(ri(start_date, end_date) / y) + 1)
        else:
            n = int(ri(start_date, end_date) / y)
        list = date_huafen(sk_code=sk_code, start_date=start_date, end_date=end_date, token=token,  n=n)
        return url_get(list)

def hg(sk_code,start_date,end_date,token):
    start_date = start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
    end_date = end_date[:4] + "-" + end_date[4:6] + "-" + end_date[6:]
    # print(sk_code)
    g_url=url1+'/us/stock/history/'+sk_code+'/'+start_date+'/'+end_date+'/'+token
    # print(g_url)
    return g_url
def ri(start_date,end_date):
    days=(datetime.datetime.strptime(end_date, '%Y%m%d') - datetime.datetime.strptime(start_date, '%Y%m%d')).days
    return days

def date_huafen(sk_code,start_date,end_date,token,n):
    import datetime
    # initializing dates
    test_date1 = datetime.datetime.strptime(start_date, '%Y%m%d')
    test_date2 = datetime.datetime.strptime(end_date, '%Y%m%d')
    # initializing N
    N = n
    temp = []
    # getting diff.
    diff = (test_date2 - test_date1) // N
    for idx in range(0, N+1):
        temp.append((test_date1 + idx * diff))

    res = []
    for sub in temp:
        res.append(sub.strftime("%Y%m%d"))
    get_list=[]
    for i in range(len(res)-1):
        if i ==len(res)-2:
            li = hg(sk_code, token=token, start_date=res[i], end_date=res[i+1])
            get_list.append(li)
        else:
            end=datetime.datetime.strptime(res[i+1], '%Y%m%d')-dateutil.relativedelta.relativedelta(days=1)
            li=hg(sk_code,token=token,start_date=res[i],end_date=end.strftime("%Y%m%d"))
            get_list.append(li)

    # print(" dates : " + str(get_list.py))
    # print(get_list.py)
    return get_list

def url_get(url_list):
    import pandas as pd
    df = pd.DataFrame(data=None)
    for item in url_list:
        # print(item)
        r =  _retry_get(item,timeout=100)
        # print(r)
        if r.empty:
           pass
        else:
            df = pd.concat([df, r], ignore_index=True)
            time.sleep(0.2)
    if df.empty:
        return df
    else:
        df = df.sort_values(by='date')  # 进行升序排序
        df.drop_duplicates(subset='date', keep='first', inplace =True, ignore_index = True)#去重

        return df

if __name__ == '__main__':
    df = daily_data(sk_code="AAPL", token='se1e7c9f1de6f161970e05ed1c10dfd2838', start_date='2003-01-08',
                    end_date='2023-09-22')
    print(df)





