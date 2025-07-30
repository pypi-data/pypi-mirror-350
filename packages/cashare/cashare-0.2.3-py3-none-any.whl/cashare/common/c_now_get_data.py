import datetime

from common.get_data import _generate_url, _retry_get


def generate_data(sk_code,mold,token,end_date:str=None,start_date='19910101',timeout=100):
    """
       获取每日数据的封装函数

       Args:
           sk_code (str): 股票代码
           token (str): 访问令牌
           start_date (str, optional): 起始日期，默认为'1991-01-01'
           end_date (str, optional): 结束日期，默认为当天日期

       Returns:
           DataFrame or str: 返回获取到的每日数据DataFrame，或者错误信息字符串
       """
    today = datetime.date.today().strftime('%Y%m%d')
    if end_date is None or end_date > today:
        end_date = today
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    if start_date > today:
        return "start_date大于现在时间"
    if start_date > end_date:
        return "start_date大于end_date"

    url = _generate_url(sk_code=sk_code, start_date=start_date, end_date=end_date, mold=mold,token=token)

    df=_retry_get(url,timeout=100)
    return df