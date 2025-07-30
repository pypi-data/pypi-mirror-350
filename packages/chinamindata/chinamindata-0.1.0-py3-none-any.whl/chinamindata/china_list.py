import requests
import pandas as pd
from chinamindata.c_min import get_token
def get_list(token=get_token(),type='stock'):
    """
    Fetch stock data from a given URL with specified parameters.

    Parameters:
    Returns:
    pd.DataFrame: A DataFrame containing the fetched stock data.
    """
    # url = "http://localhost:9002/list/"+token+'/'+type
    url="http://117.72.14.170:9002/list/"+token+'/'+type
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            # print(data)
            if data=='token无效或已超期,请重新购买':
                return data
            else:
                df = pd.DataFrame(data)
                return df
        except ValueError as e:
            print("Error parsing JSON response:", e)
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        return None

