import time

import pandas as pd

from _scratch_functions import fetch_liquor_list, fetch_page_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

HOME_URL = 'https://www.my98.com.tw'


def main():
    wine_df = None
    is_first_page = True
    start = time.time()

    liquor_list = fetch_liquor_list(HOME_URL)

    for wine, url in liquor_list.items():
        print(
            f'========================================> {wine} <========================================'
        )

        liquor_url = HOME_URL + url

        pages, wine_df = fetch_page_data(liquor_url, wine_df, is_first_page)

        if pages != None:
            for x in pages.text.splitlines():
                if x.isnumeric() and pages != '1':
                    page_url = liquor_url + f'?page={pages}'
                    wine_df = fetch_page_data(page_url, wine_df,
                                              not is_first_page)
                    time.sleep(1)

        wine_df.reset_index(drop=True, inplace=True)
        print(wine_df)

        time.sleep(2)

    print(f'Fetching Time: {time.time() - start}')


if __name__ == '__main__':
    main()
