from cashare.common.get_data import generate_data,_retry_get,handle_url
def get_c_now(sk_code, token, timeout=100):
    df = _retry_get(handle_url(type=sk_code, token=token), timeout=timeout)
    return df

if __name__ == '__main__':
    df=get_c_now(sk_code='all',token='')
    print(df)
    pass

