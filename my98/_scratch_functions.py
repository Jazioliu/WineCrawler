import json

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_liquor_df(navigableStr):
    wine_info = ''
    for cont in navigableStr:
        for s in cont:
            wine_info += s

    for r in (('cyb.push(', ''), (')', ''), ('\' ORO', ' ORO'), ('\'', '"')):
        wine_info = wine_info.replace(*r)

    wine_info = json.loads(wine_info)

    return pd.DataFrame(wine_info['ecommerce']['impressions'],
                        columns=['id', 'name', 'price', 'brand', 'category'])


def fetch_liquor_list(home_url: str):
    liquor_list = {}
    rsp = requests.get(home_url)
    home = BeautifulSoup(rsp.text, 'lxml').find('ul',
                                                attrs={
                                                    'class': 'dropdown-menu'
                                                }).find_all('a')

    for liquor in home:
        liquor_url = liquor.get('href')
        liquor_list[str(liquor_url).split('/')[-1]] = liquor_url

    return liquor_list


def fetch_page_data(web_url: str, data_frame: pd.DataFrame,
                    is_first_page: bool):
    rsp = requests.get(web_url)
    wisky = BeautifulSoup(rsp.text, 'lxml')
    scripts = wisky.find_all('script')[-1]

    if is_first_page:
        pages = wisky.find('ul', attrs={'class': 'pagination'})

        return pages, get_liquor_df(scripts)

    data_frame = data_frame.append(get_liquor_df(scripts))

    return data_frame
