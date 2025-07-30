from cashare.common.get_data import generate_data
import traceback
def get_crash_data(sk_code, token, end_date, start_date='19910101', timeout=100):
        df = generate_data(sk_code=sk_code, token=token, start_date=start_date,
                       end_date=end_date, mold='crash')
        return df
def get_daily_data(sk_code, token, end_date, start_date, timeout=100):
    df = generate_data(sk_code=sk_code, token=token, start_date=start_date,
                       end_date=end_date, mold='daily')
    return df
def get_week_data(sk_code, token, end_date, start_date, timeout=100):
    df = generate_data(sk_code=sk_code, token=token, start_date=start_date,
                       end_date=end_date, mold='week')
    return df
def get_mon_data(sk_code, token, end_date, start_date, timeout=100):
    df = generate_data(sk_code=sk_code, token=token, start_date=start_date,
                       end_date=end_date, mold='mon')
    return df

if __name__ == '__main__':

    df = get_daily_data(sk_code="000001.sz", token='a698e4b9b4747bba01599a0fcacfc994a74', start_date='1990-04-02',
                            end_date='2024-05-02')
    print(df)

    # df = get_daily_data(sk_code="000001.sz", token='', start_date='1990-04-02',
    #                     end_date='2024-05-02')
    # print(df)
    # df = get_week_data(sk_code="000001.sz", token='', start_date='1990-04-02',
    #                     end_date='2024-05-02')
    # print(df)
    # df = get_mon_data(sk_code="000001.sz", token='', start_date='1990-04-02',
    #                     end_date='2024-05-02')
    # print(df)
    #
    # pass

