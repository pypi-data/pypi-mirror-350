from cashare.common.dname import url1
#所有股票拆分日历
from cashare.common.get_data import _retry_get
from cashare.common.var_token import get_token
import pandas as pd

def sp_data(ca_code):
    li = handle_url(code=ca_code, token=get_token())
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:

        if r.empty:
            return r
        else:

            return r

def handle_url(code,token):
    g_url = url1 + '/us/stock/sp/' +code+'/'+token
    return g_url
if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df=ca.sp_data( ca_code='all')
    print(df)
    pass




