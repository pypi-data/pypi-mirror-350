from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
from cashare.common.var_token import get_token

def now_data(type):
    li = handle_url(type=type, token=get_token())
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        if r.empty:
            return r
        else:

            if r.empty:
                return r
            else:
                # 将最后一列更新为时间

                r['time'] = pd.to_datetime(r['time'], unit='s')
                return r



def handle_url(type,token):
    g_url=url1+'/us/stock/nowprice/'+type+'/'+token
    return g_url
if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df = ca.now_data(type='aapl,AA')
    print(df)




