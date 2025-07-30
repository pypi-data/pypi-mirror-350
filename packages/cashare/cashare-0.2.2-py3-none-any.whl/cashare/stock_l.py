import httpx
import requests

from cashare.common.dname import url1
import pandas as pd
from cashare.common.var_token import get_token

from cashare.common.get_data import _retry_get
def stock_list(type:str,):
    if type in['us','hk','ca','eu','tsx','cp','index','etf','fx']:
        url = url1 + '/stock/list/'+type+'/'+ get_token()
        # print(url)
        # r = _retry_get(url, timeout=100)
        # return r
        r=requests.get(url)
        json_data = r.json()
        return pd.DataFrame(json_data)

    else:
        return "type输入错误"

if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df = ca.stock_list(type='hk', )
    print(df)
    df = ca.stock_list(type='us', )
    print(df)
    pass



