import csv
from selenium import webdriver, common
import chromedriver_binary  # Adds chromedriver binary to path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

writer = csv.writer(open('newses.csv', 'w'))
writer.writerow(['URL', "Date", 'Headline', 'Content', 'Portal'])

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
driver2 = webdriver.Chrome(options=options)

page = 1

while True:
    driver.get('https://www.thedailystar.net/tags/road-accident?page='+str(page))

    links = driver.find_element_by_class_name('view-content').find_elements_by_css_selector('h3>a')

    for url in links:
        url = url.get_attribute('href')
        driver2.get(url)

        headline = driver2.find_element_by_xpath('//h1[@itemprop="headline"]').text
        content = driver2.find_elements_by_class_name('article-section')[0].find_element_by_class_name('section-content').text
        date = driver2.find_element_by_css_selector('.date.text-10').text
        comma = date.find(',')
        date = date[4:comma+6]
        print(date)

        writer.writerow([url, date, headline, content, "Dailystar"])

    page += 1