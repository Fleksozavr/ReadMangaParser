import asyncio
import os
import img2pdf
import time

from headers.parse.page.save_html_page import Chrome
from headers.parse.page.parse_page import download_images_from_html
from headers.parse.title.save_html_title import Title
from headers.parse.title.parse_title import parse_titles


async def save_images_to_pdf(chapter_folder):
    results_folder = 'results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    pdf_filename = os.path.join(results_folder, os.path.basename(chapter_folder) + '.pdf')
    image_files = []

    for root, _, files in os.walk(chapter_folder):
        for file in files:
            if file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                image_files.append(img_path)

    if image_files:
        with open(pdf_filename, 'wb') as f:
            f.write(img2pdf.convert(image_files, layout_fun=img2pdf.get_layout_fun((img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)))))
        print(f'PDF-файл успешно сохранен как {pdf_filename}')
    else:
        print(f'В папке {chapter_folder} не найдено изображений для конвертации в PDF')


async def save_and_parse_title_html(url_title):
    title = Title()
    title.save_title_html(url_title, filename='title_page.html')
    parse_titles('html/title_page.html')


async def save_page_manga(url_mangas):
    chrome = Chrome()
    image_folders = []

    try:
        for url_manga in url_mangas:
            filename = url_manga.split('/')[-1] + '.html'
            chrome.save_manga_html(url_manga, filename)
            html_path = os.path.join('html', filename)
            output_folder = html_path.replace('.html', '_images')
            await download_images_from_html(html_path, output_folder)
            image_folders.append(output_folder)

        for folder in image_folders:
            await save_images_to_pdf(folder)
    finally:
        chrome.quit_browser()


async def main():
    try:
        url_title = input('Введите URL тайтла: ')
        await save_and_parse_title_html(url_title)

        num_chapters = int(input('Введите количество глав для скачивания: '))
        url_mangas = [input(f'Введите ссылку на главу {i + 1}: ') for i in range(num_chapters)]
        await save_page_manga(url_mangas)

    except KeyboardInterrupt:
        print('Скрипт был остановлен')
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"\nВнимание: {e}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена пользователем")
    except Exception as e:
        print(f"Произошла критическая ошибка: {e}")