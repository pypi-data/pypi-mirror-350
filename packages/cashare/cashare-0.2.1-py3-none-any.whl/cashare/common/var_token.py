
import pandas as pd
import os

BK = 'bk'

def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'ca.csv')
    df.to_csv(fp, index=False)

def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'ca.csv')
    if os.path.exists(fp):

        df = pd.read_csv(fp)


        return str(df.loc[0]['token'])
    else:
        print("请设置token")
        return None