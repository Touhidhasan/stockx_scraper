import csv
import pandas as pd
import requests
from datetime import datetime


# _pxvid


# write header of the csv
csvfile_name="output.csv"
with open(csvfile_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Date','Size','Sale price'])

headers1 = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://stockx.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://cdn.cookielaw.org/consent/137eafd0-59e4-44a7-a76f-e26ddbde8f33/0192f800-42ed-7cb1-9f72-2f938ff8fd08/en.json',
    headers=headers1,
)

# print(response.text)

json_response=response.json()

cookies_all=json_response['DomainData']['Groups'][5]['FirstPartyCookies']

for cookie_pxvid in cookies_all:
    if cookie_pxvid['Name'] =='_pxvid':
        _pxvid=cookie_pxvid['id']
        print(_pxvid)


cookies = {
    'stockx_device_id': '',
    'stockx_session_id': '',
    'stockx_session': '',
    'language_code': 'en',
    'stockx_selected_region': 'US',
    'stockx_preferred_market_activity': 'sales',
    'stockx_product_visits': '1',
    'display_location_selector': 'false',
    'chakra-ui-color-mode': 'light',
    'is_gdpr': 'false',
    'stockx_ip_region': 'US',
    'pxcts': '',
    '_pxvid': _pxvid,
    '_pxde': '',
    '_dd_s': '',
    'OptanonConsent': '',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'apollographql-client-name': 'Iron',
    'apollographql-client-version': '2025.01.19.00',
    'app-platform': 'Iron',
    'app-version': '2025.01.19.00',
    'content-type': 'application/json',
    'origin': 'https://stockx.com',
    'priority': 'u=1, i',
    'referer': 'https://stockx.com/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'selected-country': 'US',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-operation-name': 'GetProductMarketSales',
    'x-stockx-device-id': '',
    'x-stockx-session-id': '',
}

json_data = {
    'query': 'query GetProductMarketSales($productId: String!, $currencyCode: CurrencyCode, $market: String, $first: Int, $isVariant: Boolean!, $viewerContext: MarketViewerContext) {\n  product(id: $productId) @skip(if: $isVariant) {\n    id\n    market(currencyCode: $currencyCode) {\n      ...MarketSalesFragment\n    }\n  }\n  variant(id: $productId) @include(if: $isVariant) {\n    id\n    market(currencyCode: $currencyCode) {\n      ...MarketSalesFragment\n    }\n  }\n}\n\nfragment MarketSalesFragment on Market {\n  sales(first: $first, market: $market, viewerContext: $viewerContext) {\n    edges {\n      cursor\n      node {\n        amount\n        associatedVariant {\n          id\n          traits {\n            size\n          }\n        }\n        sameFees\n        createdAt\n        orderType\n      }\n    }\n  }\n}',
    'variables': {
        'productId': 'fear-of-god-essentials-hoodie-fw22-light-oatmeal',
        'market': 'US',
        'viewerContext': 'BUYER',
        'currencyCode': 'USD',
        'first': 50,
        'isVariant': False,
    },
    'operationName': 'GetProductMarketSales',
}

response = requests.post('https://stockx.com/api/p/e', cookies=cookies, headers=headers, json=json_data)

# print(response.text)

json_response=response.json()

items=json_response['data']['product']['market']['sales']['edges']

for item in items:
    sale_price=item['node']['amount']
    print(sale_price)

    p_id=item['node']['associatedVariant']['id']
    print(p_id)

    size=item['node']['associatedVariant']['traits']['size']
    print(size)

    date_str=item['node']['createdAt']
    date=date_str


    # convert date format
    # try:
    #     dt_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    # except:
    #     dt_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    # date = dt_object.strftime('%m/%d/%y, %I:%M %p')
    # print(date)

    # check duplicate
    # df = pd.read_csv('output.csv')
    # exists_in_csv = df[(df.iloc[:, 0] == p_id) & (df.iloc[:, 1] == date) & (df.iloc[:, 2]  == size) & (df.iloc[:, 3]  == sale_price)].shape[0] > 0
    # if not exists_in_csv:

    # write the result in csv
    with open(csvfile_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date,size,sale_price])
    # else:
    #     print('Already exist')