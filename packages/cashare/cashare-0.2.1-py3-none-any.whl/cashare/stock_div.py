from cashare import get_token
from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
#个股股息
def div_data(ca_code):
    li = handle_url(code=ca_code, token=get_token())
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        if r.empty:
            return r
        else:
            r["date"] = pd.to_datetime(r["date"], unit='ms')
            return r

def handle_url(code,token):
    g_url=url1+'/us/stock/s_d_history/'+code+'/'+token
    return g_url
if __name__ == '__main__':
    import cashare as ca
    ca.set_token('you_token')
    df=ca.div_data(ca_code='AA')
    # missing_rows = df.isnull().any(axis=1)
    #
    # # 计算总共有多少行存在缺失值
    # num_missing_rows = missing_rows.sum()
    #
    # print(f"存在数据不全的行数：{num_missing_rows}")

    total_rows = len(df)
    print(f"总行数：{total_rows}")

    # 检测存在空值的行
    missing_rows = df[df.isnull().any(axis=1)]

    if not missing_rows.empty:
        # 存在空值的行索引（列表）
        missing_indices = missing_rows.index.tolist()
        # 空值行的起始和结束索引
        start_idx = missing_indices[0]
        end_idx = missing_indices[-1]
        # 输出空值行范围和数量
        print(f"存在空值的行索引范围：从第 {start_idx} 行到第 {end_idx} 行")
        print(f"具体空值行索引：{missing_indices}")
        print(f"存在数据不全的行数：{len(missing_rows)}")
    else:
        print("没有空值行！")

    print(df)


