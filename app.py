import pygsheets
import pandas as pd
import requests
import schedule
import time


def req():
    #   GET request to API, returns data as JSON
    urlr = "/coins/markets"
    url = "https://api.coingecko.com/api/v3" + urlr
    p = {'vs_currency': 'usd',
         'order': 'market_cap_desc',
         'per_page': '100',
         'page': '1',
         'sparkline': 'false'
         }
    res = requests.get(url, params=p)
    json_data = res.json()
    return json_data
# json_data: <class 'list'>
# json_data[0]: <class 'dict'>


def create_headers(json_data):
    # Creates headers for the spreadsheet
    headers = []
    for key in json_data[0].keys():
        headers.append(key)
    return headers


def format_data(json_data, header):
    # Parse the data to fit the google drive format and make it usable to export into a spreadsheet
    result = []
    for coin in json_data:
        for key, value in coin.items():
            if key == header:
                result.append(value)
    return result


def create_table(json_data):
    # Main function, uses the others to post the data into the spreadsheet

    # authorization
    gc = pygsheets.authorize(
        service_file=r"C:\Users\Victor\Documents\Code\CryptoPunk\cryptopunk-328117-49ef93e13f5b.json")

    # Create empty dataframe
    df = pd.DataFrame()
    headers = create_headers(json_data)

   # Create a columns
    for header in headers:
        data = format_data(json_data, header)
        df[header] = data

    # open the google spreadsheet
        sh = gc.open('data')

    # select the first sheet
        wks = sh[0]

    # update the first sheet with df, starting at cell B2.
        wks.set_dataframe(df, (1, 1))
    print("Updating spreadsheet")


data = req()
schedule.every().minute.do(create_table, json_data=data)


print(schedule.get_jobs())
while True:
    schedule.run_pending()
    time.sleep(1)
