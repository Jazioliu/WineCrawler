import time

import pandas as pd
from common import fetch_page_data

from config import WINE_URL

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def main():
    wine_df = None
    is_first_page = True
    start = time.time()

    for wine, url in WINE_URL.items():
        print(
            f'========================================> {wine} <========================================'
        )

        pages, wine_df = fetch_page_data(url, wine_df, is_first_page)

        if pages != None:
            for x in pages.text.splitlines():
                if x.isnumeric() and pages != '1':
                    page_url = url + f'?page={pages}'
                    wine_df = fetch_page_data(page_url, wine_df,
                                              not is_first_page)

        wine_df.reset_index(drop=True, inplace=True)
        print(wine_df)

        time.sleep(2)

    print(f'Fetching Time: {time.time() - start}')


if __name__ == '__main__':
    main()
