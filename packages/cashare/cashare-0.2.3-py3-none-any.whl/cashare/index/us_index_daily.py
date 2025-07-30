from cashare.common.dname import url1
import datetime
import pandas as pd
from cashare.common.get_data import _retry_get
from cashare.common.var_date import check_date
from cashare.common.var_token import get_token

def index_daily(ca_code,end_date=str(datetime.date.today().strftime('%Y%m%d')),start_date='19000101',x=5000, y=5000):

    ls=check_date(start_date=start_date,end_date=end_date)
    if isinstance(ls, str):
        return ls
    else:
        start_date=ls[0]
        end_date=ls[1]

    li = hg(ca_code=ca_code, token=get_token(), start_date=start_date, end_date=end_date)
    r = _retry_get(li, timeout=100)
    if type(r)==str:
        return r
    else:
        # print(r)
        if r.empty:
            return r
        else:
            r["date"] = pd.to_datetime(r["date"], unit='ms')
            return r


def hg(ca_code,start_date,end_date,token):
    start_date = start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
    end_date = end_date[:4] + "-" + end_date[4:6] + "-" + end_date[6:]
    g_url=url1+'/us/index/history/'+ca_code+'_index/'+start_date+'/'+end_date+'/'+token
    return g_url


if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df = ca.index_daily(ca_code="VIX", start_date='2023-06-05',end_date='2025-09-22')
    print(df)








