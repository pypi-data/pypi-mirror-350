# SHEETS_BROWSER 

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests

import os, re
from time import sleep

URL_PATTERN = r'^(?:https?:\/\/)?musescore\.com\/user\/\d+\/scores\/\d+$'

CHROME_OPTIONS = ['--no-sandbox','--log-level=3']

PAGE_LOAD_TIMEOUT=20

# Different browsers

import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",  # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",  # Edge
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",  # Safari
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36" # Android Chrome
]

def create_driver_with_random_user_agent():
    """Создает экземпляр WebDriver с случайным User-Agent."""

    user_agent = random.choice(user_agents)

    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")  # Headless mode

    #service = Service(executable_path="/путь/к/вашему/chromedriver")  # Замените на актуальный путь
    driver = webdriver.Chrome(options=options)
    

    return driver


driver = create_driver_with_random_user_agent()


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
        print(driver.title)
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

# IMAGES_TO_PDF

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def create_pdf_from_images(image_dir, destination, pdf_name):

    print("> Creating PDF... ", end='')

    c = canvas.Canvas(os.path.join(destination, pdf_name) + ".pdf", pagesize=letter)
    c.setTitle(pdf_name)

    image_index = 0
    while True:
        png_filename = os.path.join(image_dir, f"sheet_{image_index}.png")
        svg_filename = os.path.join(image_dir, f"sheet_{image_index}.svg")

        if os.path.exists(png_filename):
            try:
                img = Image.open(png_filename)
                img_width, img_height = img.size
                c.setPageSize((img_width, img_height))
                c.drawImage(png_filename, 0, 0)  # Рисуем PNG
                c.showPage() # Закрываем страницу

            except Exception as e:
                print(f"Ошибка при обработке PNG {png_filename}: {e}")
                break

        elif os.path.exists(svg_filename):
            try:
                drawing = svg2rlg(svg_filename)
                # масштабируем drawing
                scale_x = letter[0] / drawing.width
                scale_y = letter[1] / drawing.height
                scale = min(scale_x, scale_y)
                drawing.scale(scale, scale)
                renderPDF.draw(drawing, c, 0, 0) #Рисуем SVG
                c.showPage() #Закрываем страницу
            except Exception as e:
                print(f"Ошибка при обработке SVG {svg_filename}: {e}")
                break
        else:
            # Нет файла, заканчиваем
            break

        image_index += 1 #Переходим к следующему файлу
        
    c.save()
    print(f"success!")


# MAIN



raw_dir = "RAW"
pdf_dir = "PDF"


def clear_folder(folder_path):

    print(f"> Cleaning folder '{folder_path}'... ", end='')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
        except Exception as e:
            print(f"> Failed to remove {file_path}. Reason: {e}")
    
    print("finished!")


def set_save_dir(dir):
    global pdf_dir
    pdf_dir = dir


def save_score(url):

    os.makedirs(raw_dir, exist_ok=True)
    
    if pdf_dir:
        os.makedirs(pdf_dir, exist_ok=True)
    else:
        raise Exception("PDF save directory is not defined! Use 'set_save_dir(dir)' before.")

    # Открываем страницу
    sheets_name = load_page(url)

    if (sheets_name == None):   # Если всё плохо, то ничего не делаем
        return None

    # Проверяем, может мы уже качали такие ноты
    if os.path.exists(os.path.join(pdf_dir, sheets_name + ".pdf")):
        return os.path.join(pdf_dir, sheets_name + ".pdf")

    # Загружаем ноты в папку
    load_sheets(url, raw_dir)

    # Склеиваем ноты
    create_pdf_from_images(raw_dir, pdf_dir, sheets_name)

    # Очищаем папку с картинками
    clear_folder(raw_dir)

    return os.path.join(pdf_dir, sheets_name + ".pdf")


if __name__ == "__main__":
    set_save_dir("PDF")

    url = input("Enter URL to score from MusicScore: ")
    path = save_score(url)
    
    if path != None:
        print(f"> Saved to '{path}'")