import locale
import datetime

def convertMoney(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    money = locale.currency(value, grouping=True, symbol=None)
    return money

def tomorrowDay():
    date_now = datetime.datetime.now()
    tomorrow_date = date_now + datetime.timedelta(days=1)
    return tomorrow_date.strftime("%d/%m/%y20")