from _datetime import datetime, timezone, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import time
import getpass


def run(email, pw):
    browser = webdriver.Edge()

    browser.get('https://banking.quirion.de/login')
    WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, '#username'))
    browser.find_element(By.CSS_SELECTOR, '#username').send_keys(email)
    browser.find_element(By.CSS_SELECTOR, '#password').send_keys(pw)
    browser.find_element(By.CSS_SELECTOR, '#content > div > div > div.container.info > div > form > div > button.go_on._button_b96kp_1').click()
    time.sleep(2)

    values = []
    WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR,'#content > div > div._content_66ynt_25 > div.IpsHistory._screen_66ynt_1 > div._content_66ynt_25 > div > div.echarts-for-react > div:nth-child(2)'))
    tz = timezone(timedelta(hours=+2))
    days = 2 if datetime.today().weekday() != 6 else 3
    while len(values) < 1 or get_time(values[-1]) <= time.mktime(datetime.now(tz).timetuple())-(60*60*24*days)-(60*60):
        value = browser.find_element(By.CSS_SELECTOR, '#content > div > div._content_66ynt_25 > div.IpsHistory._screen_66ynt_1 > div._content_66ynt_25 > div > div.echarts-for-react > div:nth-child(2)').text.split('\n')
        if value != ['']:
            values.append(value)

    values = unique(values)
    f = open("output.csv", "w")
    f.write('Datum;Kurs;Höchst;Tiefst;Umsatz\n')
    for value in values:
        current = float(value[1].replace('Wert: ', '').replace(' €', '').replace('.', '').replace(',', '.'))
        sum = float(value[2].replace('Eingezahlt: ', '').replace(' €', '').replace('.', '').replace(',', '.'))
        f.write(datetime.fromtimestamp(get_time(value)).strftime('%d.%m.%Y')+';' + "{:.3f}".format(current*100/sum).replace('.', ',') + ';;;\n')
    f.close()


def get_time(value):
    months = {'Januar': 'January', 'Februar': 'February', 'März': 'March', 'Mai': 'May', 'Juni': 'June', 'Juli': 'July', 'Oktober': 'October', 'Dezember': 'December'}
    date = value[0]
    for key in months:
        date = date.replace(key, months.get(key))
    if date[1] == '.':
        date = '0' + date
    return datetime.timestamp(datetime.strptime(date, "%d. %B %Y"))


def unique(it) -> []:
    dates = []
    values = []
    previous = ''
    for el in it:
        if get_time(el) not in dates and el[1] != previous:
            dates.append(get_time(el))
            values.append(el)
            previous = el[1]

    return values


if __name__ == '__main__':
    username = input('username:', )
    pw = getpass.getpass('password:', )
    run(username, pw)
