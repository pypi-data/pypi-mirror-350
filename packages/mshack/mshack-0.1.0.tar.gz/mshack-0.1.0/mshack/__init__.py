from sheets_browser import load_sheets, load_page
from images_to_pdf import create_pdf_from_images
import os


raw_dir = "SHEETS RAW"
pdf_dir = None


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