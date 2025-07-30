
#全部接口测试
you_token='se1e7c9f1de6f161970e05ed1c10dfd2838'
from cashare.daily import daily_data




# 计算执行时间（秒）


df = daily_data(sk_code="AAPL", token=you_token, start_date='2002-04-02',
                    end_date='2023-09-02')




print('美股个股日线',df)

df = daily_data(sk_code="0001.HK", token=you_token, start_date='2002-04-02',
                    end_date='2023-09-02')
print('港股个股日线',df)
from cashare.mc_data import mark_c_data
df=mark_c_data(code='AAPL',token=you_token,start_date='2012-09-09',end_date='-09-09')

print('美股个股市值',df)

df=mark_c_data(code='0001.HK',token=you_token,start_date='2002-09-09',end_date='2022-09-09')

print('港股个股市值',df)


from cashare.minute_data import m_data
df=m_data(sk_code="AAPL",token=you_token,type='30min',start_date='2023-03-02',end_date='2023-05-02')
print('美股分钟线',df)

from cashare.minute_data import m_data
df=m_data(sk_code="AAQC-UN",token=you_token,type='30min',start_date='2023-03-02',end_date='2023-05-02')



from cashare.stock_l import stock_list

df=stock_list(type='hk',token=you_token)
print('港股列表',df)


from cashare.minute_data import m_data
df=m_data(sk_code="0001.HK",token=you_token,type='30min',start_date='2023-03-02',end_date='2023-05-02')
print('美股分钟线',df)

df=stock_list(type='us',token=you_token)
print('美股列表',df)
df=stock_list(type='eu',token=you_token)
print('欧洲交易所列表',df)
df=stock_list(type='tsx',token=you_token)
print('多伦多列表',df)
# df=stock_list(type='fx',token=you_token)
# print('外汇列表',df)
df=stock_list(type='etf',token=you_token)
print('全球ETF列表',df)


from cashare.daily import daily_data

df = daily_data(sk_code="AAPL", token=you_token, start_date='2022-04-02',
                    end_date='2023-05-02')
print('美股个股日线',df)

# df = daily_data(sk_code="0001.HK", token=you_token, start_date='2022-04-02',
#                     end_date='2023-05-02')
# print('港股个股日线',df)
#
#
# from cashare.minute_data import m_data
# df=m_data(sk_code="AAPL",token=you_token,type='30min',start_date='2023-03-02',end_date='2023-05-02')
# print('美股分钟线',df)
#
#
# df=m_data(sk_code="0001.HK",token=you_token,type='30min',start_date='2023-03-02',end_date='2023-05-02')
# print('港股分钟线',df)


from cashare.stock_now import now_data
# df=now_data(type='us',token=you_token)
# print('美国全部实时',df)
df=now_data(type='hk',token=you_token)
print('香港全部实时',df)
df=now_data(type='eu',token=you_token)
print('欧洲全部实时',df)
df=now_data(type='tsk',token=you_token)
print('多伦多全部实时',df)
df=now_data(type='cp',token=you_token)
print('加密货币全部实时',df)
df=now_data(type='index',token=you_token)
print('全球指数实时',df)
df=now_data(type='fx',token=you_token)
print(df)
print('外汇全部实时',df)
df=now_data(type='AAPL',token=you_token)
print('个股实时',df)

#获取单个股票市值
from cashare.mc_data import mark_c_data
df=mark_c_data(code='AAPL',token=you_token,start_date='2012-09-09',end_date='2022-09-09')

print('美股个股市值',df)

df=mark_c_data(code='0001.HK',token=you_token,start_date='2002-09-09',end_date='2022-09-09')

print('港股个股市值',df)

#个股技术指标：
from cashare.ti_data import ti_data
df=ti_data(ma='6_ema',sk_code="aapl",token=you_token,type='1min',start_date='2023-09-21',end_date='2023-09-24')
print('美股个股技术指标',df)

df=ti_data(ma='5_wa',sk_code="0001.HK",token=you_token,type='1min',start_date='2023-09-21',end_date='2023-09-24')
print('港股个股技术指标',df)


#股票拆分日历
from cashare.stock_sp import sp_data
df = sp_data(token=you_token, end_date='2023-09-08', start_date='2023-02-01', )
print('股票拆分日历',df)


# 个股股息
from cashare.stock_div import sd_data
df=sd_data(code='aapl',token=you_token)
print('美股个股股息',df)


df=sd_data(code='0001.HK',token=you_token)
print('港股个股股息',df)


#经济数据：
# 美债
from cashare.econ import eco

df = eco(start_date='2021-01-01', end_date='2023-03-09', type='treasury', token=you_token)
print('美债数据',df)
df = eco(start_date='2021-01-01', end_date='2023-03-09', type='CPI', token=you_token)
print('CPI',df)
df = eco(start_date='2021-01-01', end_date='2023-03-09', type='GDP', token=you_token)
print('GDP',df)

#大A实时接口
from cashare.stock.c_now import get_c_now
df=get_c_now(sk_code='all',token=you_token)
print('大A全部实时数据',df)

df=get_c_now(sk_code='000001',token=you_token)
print('个股实时数据',df)

from cashare.income import income_data
from cashare.balance import balance
from cashare.cash_flow import cash_flow
df = income_data(sk_code='AAPL',period='annual',token=you_token)
print(df)
df=balance(sk_code='AAPL',period='annual',token=you_token)
print(df)
df=cash_flow(sk_code='AAPL',period='annual',token=you_token)
print(df)









