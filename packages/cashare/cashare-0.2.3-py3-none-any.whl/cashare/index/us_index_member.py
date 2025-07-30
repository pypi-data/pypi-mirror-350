from cashare.common.dname import url1
import datetime
import pandas as pd
from cashare.common.get_data import _retry_get
from cashare.common.var_date import check_date
from cashare.common.var_token import get_token

def index_member(ca_code,):



    li = hg(ca_code=ca_code, token=get_token())
    r = _retry_get(li, timeout=100)
    # print(r)
    r["add_date"] = pd.to_datetime(r["add_date"], unit='ms')
    r.drop(["industry"], axis=1, inplace=True)
    return r



def hg(ca_code,token):

    g_url=url1+'/us/index/contain/'+ca_code+'_include/'+token
    return g_url


if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df = ca.index_member(ca_code="spx",)
    print(df)
    # df.to_csv('ndx_include1.csv')
    ##spx Djia ndx







