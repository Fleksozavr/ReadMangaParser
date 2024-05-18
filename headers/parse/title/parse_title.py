import os

from bs4 import BeautifulSoup


def parse_titles(filename):
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не существует.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    titles = soup.select("td.item-title a")

    if not titles:
        print("Не найдено ни одного заголовка.")
        return

    for title in titles:
        title_text = title.text.strip()
        title_url = "https://readmanga.live" + title['href']
        print(f"Название: {title_text}")
        print(f"Ссылка: {title_url}")
