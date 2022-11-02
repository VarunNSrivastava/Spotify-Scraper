from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import re


def find_dates(main_soup):
    # song = main_soup.find_all('div', {'aria-rowindex': '2'})[0]
    # date = song.find_all('div', {'aria-colindex': 4})[0]
    i = 2
    is_next = True
    all_dates = []
    while is_next:
        curr_list = main_soup.find_all('div', {'aria-rowindex': str(i)})
        if len(curr_list):
            song = curr_list[0]
            date = song.find_all('div', {'aria-colindex': 4})[0]
            all_dates.append(date.text)
        is_next = len(curr_list)
        i += 1

    return all_dates


def get_dates(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=chrome_options)  # executable_path="/Users/varun/Downloads/chromedriver")\
    driver.get(url)
    sleep(10)
    driver.execute_script("document.body.style.zoom = '0.01'")
    sleep(20)

    dates = driver.find_elements(By.XPATH, "//div[@aria-colindex='4']")
    print([date.text for date in dates])
    print(len(dates))
    return [date.text for date in dates[1:]]


def process_dates(dates):
    parsed = []
    for date in dates:
        if "ago" in date:
            k = int(date.split()[0])
            tod = datetime.datetime.now()
            d = datetime.timedelta(days=k)
            parsed.append(tod - d)
        else:
            d = datetime.datetime.strptime(date, '%b %d, %Y')
            parsed.append(d)
    return parsed


def main():
    # wok = "https://open.spotify.com/playlist/3fP9kN7B8yvHOlzEPY2jIK?si=266fde04aca44e2e"
    # baby = "https://open.spotify.com/playlist/3zNoq1vbnqD7tQFMzIVvzu?si=0f4e7c02cae04217"
    # dates = get_dates(baby)
    # parsed_dates = process_dates(dates)
    # np.save("baby.npy", parsed_dates, allow_pickle=True)
    # print(parsed_dates)

    baby_dates = np.load("baby.npy", allow_pickle=True)
    df = pd.DataFrame({"datetime": baby_dates})
    fig, ax = plt.subplots()
    df["datetime"].astype(np.int64).plot.hist(ax=ax, bins=24)
    labels = ax.get_xticks().tolist()
    print(labels)
    labels = pd.to_datetime(labels)
    new_labels = [f"{label.month}/{label.day}" for label in labels]
    ax.set_xticklabels(new_labels, rotation=30)
    plt.show()

if __name__ == '__main__':
    main()
