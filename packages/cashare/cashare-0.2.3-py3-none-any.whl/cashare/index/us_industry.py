from cashare.common.dname import url1
import datetime
import pandas as pd
from cashare.common.get_data import _retry_get
from cashare.common.var_date import check_date
from cashare.common.var_token import get_token

def industry():

    li = hg( token=get_token())
    r = _retry_get(li, timeout=100)
    if type(r)==str:
        return r
    else:
        # print(r)
        return r



def hg(token):

    g_url=url1+'/us/hangye/us'+'/'+token
    return g_url


if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df = ca.industry()
    print(df)








