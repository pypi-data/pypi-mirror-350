import httpx
from cashare.common.dname import url1
import datetime
import pandas as pd
from httpx import HTTPStatusError
from tenacity import retry, stop_after_attempt, wait_fixed,retry_if_exception_type
# import requests
# from io import StringIO
# import json
@retry(stop=stop_after_attempt(4),wait=wait_fixed(25),retry=retry_if_exception_type(Exception))
def _retry_get(url,timeout):
    """
    带重试机制的GET请求函数

    Args:
        url (str): 请求的URL

    Returns:
        Response: 请求的响应对象

    """
    try:
        with  httpx.Client(timeout=timeout) as client:  # ，读取时间30s#解决timeout问题
            response = client.get(url, timeout=timeout)

        # response = httpx.get(url,timeout=timeout)
        response.raise_for_status()  # 检查响应状态码
        json_data = response.json()
        if json_data == 'token无效或已超期':
            return json_data
        else:
            # print(pd.DataFrame(json_data))

            return pd.DataFrame(json_data)


        # response = requests.get(url, stream=True)

        # if format == "csv":
        #     # CSV 流式处理
        #     chunks = []
        #     for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
        #         buffer = StringIO(chunk)
        #         df_chunk = pd.read_csv(buffer)
        #         chunks.append(df_chunk)
        #     return pd.concat(chunks, ignore_index=True)
        #
        # elif format == "json":
        #     # JSON Lines 处理
        # data = []
        # for line in response.iter_lines():
        #     if line:
        #         # try:
        #         data.append(json.loads(line.decode("utf-8")))
        #         # except json.JSONDecodeError:
        #         #     print(f"无效 JSON 行: {line}")
        # return pd.DataFrame(data)



    except httpx.RequestError as e:

        # 处理网络请求失败的异常
        print("网络请求失败：" + str(e))

        raise Exception("网络请求失败：" + str(e))
    except HTTPStatusError as e:
        # print(e)
        # 处理 HTTP 状态错误的异常
        print("请求失败,请排查自己网络是否可以上网后，再联系管理员,错误代码：" + str(e.response.status_code))
        raise Exception("请求失败：" + str(e.response.status_code))




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

def _generate_url(sk_code, start_date, end_date, token,mold, limit=10000):
    """
    生成URL的辅助函数

    Args:
        sk_code (str): 股票代码
        start_date (str): 起始日期
        end_date (str): 结束日期
        token (str): 访问令牌
        limit (int, optional): 获取数据的条数，默认为10000
        type (str): 访问令牌

    Returns:
        str: 生成的URL
    """
    url = f"{url1}/stock/{mold}/{sk_code}/{start_date}/{end_date}/{limit}/{token}"

    return url


def handle_url(type,token):
    type=type[:6]
    g_url=url1+'/stock/c_now/'+type+'/'+token

    return g_url

if __name__ == '__main__':

    df = generate_data(sk_code="000001.sz", token='you_token', start_date='1990-04-02',
                        end_date='2024-05-02',mold='daily')
    print(df)

