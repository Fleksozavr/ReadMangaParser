import os
import aiohttp
import aiofiles
import asyncio

from bs4 import BeautifulSoup


async def download_image(session, img_src, img_filename, data_page):
    try:
        async with session.get(img_src) as response:
            if response.status == 200:
                async with aiofiles.open(img_filename, 'wb') as file:
                    await file.write(await response.read())
                    await asyncio.sleep(1)
                print(f"Изображение {data_page} скачано и сохранено как {img_filename}")
            else:
                print(f"Не удалось скачать изображение {data_page}: {response.status}")
    except aiohttp.ClientConnectorError as e:
        print(f"Ошибка подключения при попытке скачать изображение {data_page}: {e}")
    except asyncio.TimeoutError:
        print(f"Таймаут при попытке скачать изображение {data_page}")


async def download_images_from_html(html_path, output_folder):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"Файл {html_path} не найден")
        return

    if not html_content:
        print("HTML контент пустой")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    imgs = soup.find_all('img', id='mangaPicture')

    if not imgs:
        print("Не найдено ни одного изображения с id 'mangaPicture'")
        return

    timeout = aiohttp.ClientTimeout(total=30)

    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for img in imgs:
            data_page = img.get('data-page')
            img_src = img.get('src')
            if img_src:
                img_folder = os.path.join(output_folder, f"image_{data_page}")
                if not os.path.exists(img_folder):
                    os.makedirs(img_folder)
                img_filename = os.path.join(img_folder, f"image_{data_page}.jpg")
                await download_image(session, img_src, img_filename, data_page)
            else:
                print(f"Не найден src у изображения в data-page={data_page}")
