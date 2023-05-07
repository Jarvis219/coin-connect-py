from datetime import datetime, timedelta
from constans import token
import requests

coinHeaders = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

currentDay = datetime.now().strftime("%Y-%m-%d")


def check_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_date_by_str(date_str):
    dateFormat = date_str.replace('/', '-')
    isFormat = check_date_format(dateFormat)
    if (isFormat):
        return datetime.strptime(dateFormat, '%Y-%m-%d').date()

    date_obj = datetime.strptime(dateFormat, '%d-%m-%Y')
    new_date_str = date_obj.strftime('%Y-%m-%d')
    print(new_date_str)
    return new_date_str


def get_date_by_days(days):
    today = datetime.now()
    seven_days_ago = today - timedelta(days=days)
    return seven_days_ago.strftime("%Y-%m-%d")


def get_month_ago(months):
    today = datetime.now()
    months_ago = today.replace(month=today.month-months)
    return months_ago.strftime("%Y-%m-%d")


def get_year_ago(years):
    today = datetime.now()
    years_ago = today.replace(year=today.year-years)
    return years_ago.strftime("%Y-%m-%d")


def coin_by_symbol_API(symbol, startDate, endDate, limit, headers):
    return requests.get('https://restv2.fireant.vn/symbols/' + symbol + '/historical-quotes?startDate=' +
                        str(startDate) + '&endDate=' + str(endDate) + '&offset=0&limit=' + str(limit), headers=headers)
