from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
def eco(type,start_date,end_date,token):
    '''

    :param type:treasury/
    GDP | realGDP | CPI |
    :param start_date:
    :param end_date:
    :param token:
    :return:
    '''
    if type=='treasury':
        e_list = generate_urls(url_1=url1, start_date=start_date, end_date=end_date, token=token, ty=type, interval=70,
                               y=70)

        return url_get(e_list)

    else:
        li = handle_url(start_date=start_date, end_date=end_date, type=type, token=token)
        r = _retry_get(li, timeout=100)
        if str(r) == 'token无效或已超期':
            return r
        else:
            return r


def handle_url(start_date,end_date,type,token):
    g_url=url1+'/'+type+'/'+start_date+'/'+end_date+'/'+token

    return g_url

from datetime import datetime, timedelta


def url_get(url_list):
    import pandas as pd
    df = pd.DataFrame(data=None)
    for item in url_list:
        r = _retry_get(item, timeout=100)
        if r.empty:
            pass
        else:
            lsss = r.sort_values(by='date')  # 进行升序排序
            df = pd.concat([df, lsss], ignore_index=True)
    df.drop_duplicates(subset='date', keep='first', inplace=True, ignore_index=True)  # 去重

    return df
def generate_urls(url_1,ty,start_date, end_date, interval, y,token):
    urls = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if (end_date - current_date).days < y:
        url = f"{url_1}/{ty}/{start_date}/{end_date.strftime('%Y-%m-%d')}/{token}"
        urls.append(url)

    else:
        while current_date <= end_date:

            url_end_date = current_date + timedelta(days=interval - 1)
            if url_end_date > end_date:
                url_end_date = end_date
            url = f"{url_1}/{ty}/{current_date.date()}/{url_end_date.strftime('%Y-%m-%d')}/{token}"
            urls.append(url)
            current_date += timedelta(days=interval)
    return urls




# urls = generate_urls(start_date = "2022-08-15", end_date = "2023-09-04", interval=7, y=30,url_1='https://192.178')
# print(urls)
if __name__ == '__main__':
    ll=eco(start_date='2021-01-01',end_date='2023-03-09',type='treasury',token='you_token')
    print(ll)
