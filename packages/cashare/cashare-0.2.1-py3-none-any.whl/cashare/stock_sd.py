from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
#个股股息
def sd_data(code,token):
    li = handle_url(code=code, token=token)
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        return r
def handle_url(code,token):
    g_url=url1+'/us/stock/s_d_history/'+code+'/'+token
    return g_url
if __name__ == '__main__':
    df=sd_data(code='AAPL',token='you_token')
    print(df)


