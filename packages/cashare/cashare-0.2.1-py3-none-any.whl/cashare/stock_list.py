import httpx
from cashare.common.dname import url1
import pandas as pd


def stock_list(token,type:str):
    if type in['us','hk','ca','eu','tsx','cp','index','etf','fx']:
        url = url1 + '/stock/list/'+type+'/'+ token
        # print(url)
        r = httpx.get(url,timeout=100)
        return pd.DataFrame(r.json())
    else:
        return "type输入错误"

if __name__ == '__main__':
    df = stock_list(type='eu', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df=stock_list(type='hk',token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='us', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='ca', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='tsx', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='cp', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='index', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='etf', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)
    df = stock_list(type='fx', token='u698e4b9b4747bba083736e06db4b8a6a92')
    print(df)

    pass



