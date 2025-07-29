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