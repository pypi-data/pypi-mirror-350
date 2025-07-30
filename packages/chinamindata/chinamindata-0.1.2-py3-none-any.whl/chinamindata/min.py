from chinamindata.china_min_open import stk_auction_o1
from chinamindata.china_min_close import stk_auction_c1
# df = stk_auction_c(trade_date='20241122')
# print(df)

from chinamindata.china_min import pro_bar1
# df = pro_bar( code = '000001.SZ', start_date = '2024-07-07 09:00:00',
#                        end_date = '2024-07-22 15:00:00',freq='60min',)
# print(df)
class pro_api:
    def __init__(self, token=None):
        if token is not None:
            self.token = token  # 实例变量，用于内部使用或调试
            set_token(token)

        else:
            self.token = get_token()
            if self.token is None:
                raise ValueError("请设置token")
            else:
                pass


    def stk_auction_o(self,trade_date,limit='8000',offset='0'):
        return stk_auction_o1(trade_date,limit=limit,offset=offset)

    def stk_auction_c(self,trade_date,limit='8000',offset='0'):
        return stk_auction_c1(trade_date,limit=limit,offset=offset)

    def stk_mins(self,ts_code, start_date, end_date, freq='60min'):
        if freq in ['1min', '5min', '15min', '30min', '60min']:

            return pro_bar1(code=ts_code, start_date=start_date, end_date=end_date, freq=freq)
        else:
            raise ValueError("freq非法，必须是'1min','5min','15min','30min','60min'")


def pro_bar(ts_code, start_date, end_date,freq='60min'):
    if freq in ['1min','5min','15min','30min','60min']:

        return pro_bar1(code=ts_code, start_date=start_date, end_date=end_date, freq=freq)
    else:
        raise ValueError("freq非法，必须是'1min','5min','15min','30min','60min'")



import pandas as pd
import os

BK = 'bk'

def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'c_m_t.csv')
    df.to_csv(fp, index=False)


def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'c_m_t.csv')
    if os.path.exists(fp):

        df = pd.read_csv(fp)


        return str(df.loc[0]['token'])
    else:

        return "请设置token"

