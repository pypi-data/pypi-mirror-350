from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests

import os, re
from time import sleep

from config import CHROME_OPTIONS, URL_PATTERN, PAGE_LOAD_TIMEOUT


chrome_options = Options()
for arg in CHROME_OPTIONS: chrome_options.add_argument(arg)
driver = webdriver.Chrome(options=chrome_options)


def download_scores(from_url, sheets_url, dir="saved_sheets"):

    print("> Downloading scores: ")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': from_url,
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    for i in range(len(sheets_url)):

        url = sheets_url[i]

        print(f">   Score {i + 1}: ", end='')

        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Проверяем на ошибки HTTP

        print(response.status_code, end=" -> ")
        if response.status_code != 200:
            return False

        filename = f"sheet_{i}." + ("png" if url.find(".png") >= 0 else "svg")
        filepath = os.path.join(dir, filename)

        if not os.path.exists(dir):
            os.makedirs(dir)

        print(filepath)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print("> Done!")

    return True


def open_page(url):

    print(f"> Opening page '{url}'...", end=' ')

    match = re.match(URL_PATTERN, url)
    if not match:
        print(f"failed - page url is not like musicscore url")
        return False
    try:
        driver.get(url)
        print(f"success!")
        return True
    except Exception as e:
        print(f"failed: {e}")
        return False


def save_page(name):
    f = open(name + ".html", "w", encoding="utf-8")
    f.write(driver.page_source)
    f.close()


def get_sheets_urls():
    print("> Getting sheets URLs...", end=' ')
    urls = []
    outer_divs = driver.find_elements(By.ID, "jmuse-scroller-component")

    for outer_div in outer_divs:
        img_elements = outer_div.find_elements(By.TAG_NAME, "img")

        for img_element in img_elements:
            image_url = img_element.get_attribute("src")
            urls.append(image_url)
    
    print(f"recived {len(urls)} URLs")

    return urls


def get_sheets_name():

    outer_div = driver.find_element(By.ID, "aside-container-unique")

    h1_element = outer_div.find_element(By.TAG_NAME, "h1")

    span_element = h1_element.find_element(By.TAG_NAME, "span")

    span_text = span_element.text

    return span_text


def load_page(url):

    # Открываем страничку
    if not open_page(url):
        return None

    # Раскрываем, чтобы все странички появились
    driver.set_window_size(1000, 10000)

    return get_sheets_name()


def load_sheets(url, dir="tmp"):

    # Ждём выполнения JS
    print(f"> Waiting for {PAGE_LOAD_TIMEOUT} second(s)...", end=' ')
    sleep(PAGE_LOAD_TIMEOUT)
    print("go-Go-GO!")

    # Получаем URL со странички
    sheet_urls = get_sheets_urls()

    # Скачиваем все странички
    if not download_scores(url, sheet_urls, dir):
        return False

    return True