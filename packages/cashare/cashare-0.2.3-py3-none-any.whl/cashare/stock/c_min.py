from cashare.common.get_data import generate_data
import datetime
import pandas as pd

def get_min_data(sk_code,token,start_date,end_date,type,timeout=100):
    # print(start_date)
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    today = datetime.date.today().strftime('%Y%m%d')
    if end_date is None or end_date > today:
        end_date = today
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    if start_date > today:
        return "start_date大于现在时间"
    if start_date > end_date:
        return "start_date大于end_date"
    # print(start_date)

    list = get_date_list(start_date, end_date, mold=type)
    # print(list)
    result_df = pd.DataFrame()
    for i,item in enumerate(list):
        current_item = item
        # 获取下一个元素
        if i < len(list) - 1:
            next_item = list[i + 1]
            df = generate_data(sk_code=sk_code, token=token, start_date=current_item,
                               end_date=next_item, mold=type)
            # print(df)
            df['time'] = pd.to_datetime(df['time'])
            df['date'] = pd.to_datetime(df['date'])
            result_df = pd.concat([result_df, df], ignore_index=True)
        else:
            next_item = None

    if result_df.empty:
        return result_df
    else:
        df_unique = result_df.drop_duplicates()
        df_sorted=df_unique.sort_values(by='date').reset_index(drop=True)
        return df_sorted
def get_n(mold):
    if mold=='1min':
        return 50
    if mold=='5min':
        return 275
    if mold=='15min':
        return 800
    if mold=='30min':
        return 1500
    if mold == '60min':
        return 2500
def get_date_list(start_date,end_date,mold):
    n=get_n(mold)
    # initializing dates
    test_date1 = datetime.datetime.strptime(start_date, '%Y%m%d')
    # print(test_date1)
    test_date2 = datetime.datetime.strptime(end_date, '%Y%m%d')
    date_list = []
    while test_date1 <= test_date2:
        date_list.append(test_date1.strftime("%Y%m%d"))
        test_date1 += datetime.timedelta(days=n)

    ls2 = test_date2.strftime("%Y%m%d")
    date_list .append(ls2 )
    # print(date_list)
    return date_list

if __name__ == '__main__':
    df = get_min_data(sk_code="000004.sz", token='ice73c837bf196339ef2b7e946d20196057', start_date='2013-04-02',
                        end_date='2024-05-02',type='60min')
    print(df)
