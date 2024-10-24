import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import aiohttp
import asyncio

class Mighty_parser:
    def __init__(self, white_list=None, keywords=None):
        """
        Инициализация класса:
        - white_list: список сайтов, которые нужно парсить.
        - keywords: ключевые слова для фильтрации статей.
        """
        if white_list is None:
            white_list = ['https://habr.com']  # Список сайтов по умолчанию
        self.white_list = white_list

        if keywords is None:
            keywords = ['Python', 'Django', 'парсинг', 'Питон', 'Джанго']  # Ключевые слова по умолчанию
        self.keywords = keywords

    def keyword_match(self, title):
        """Проверка наличия ключевых слов в заголовке статьи."""
        return any(keyword.lower() in title.lower() for keyword in self.keywords)

    def fetch_page(self, url):
        """Загрузка страницы с помощью requests."""
        response = requests.get(url)
        return response.text

    def parse_habr(self):
        """Парсинг статей с Habr с учетом пагинации."""
        url = 'https://habr.com/ru/all/'
        matched_articles = 0
        page_number = 1

        while matched_articles < 10:
            # Обновляем URL для каждой страницы
            paginated_url = f'{url}page{page_number}/'
            page_content = self.fetch_page(paginated_url)
            soup = BeautifulSoup(page_content, 'html.parser')

            for article in soup.find_all('article'):
                title_tag = article.find('h2')
                if title_tag:
                    title = title_tag.get_text()

                    if self.keyword_match(title):
                        article_url = title_tag.find('a')['href']
                        full_article_url = urljoin(url, article_url)
                        self.parse_article(full_article_url, title)
                        matched_articles += 1
                        if matched_articles >= 10:
                            break

            page_number += 1

    def parse_article(self, full_article_url, title):
        """Парсинг отдельной статьи с Habr."""
        article_content = self.fetch_page(full_article_url)
        article_soup = BeautifulSoup(article_content, 'html.parser')

        paragraphs = article_soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)
        demo = ' '.join(article_text.split()[:200])

        # Вывод результатов
        print(f'Название: {title}')
        print(f'URL: {full_article_url}')
        print(f'Демо-версия: {demo}\n')

    async def fetch_page_async(self, session, url):
        """Асинхронная загрузка страницы."""
        async with session.get(url) as response:
            return await response.text()

    async def parse_habr_async(self):
        """Асинхронный парсинг статей с сайта Habr."""
        url = 'https://habr.com/ru/all/'
        async with aiohttp.ClientSession() as session:
            page_content = await self.fetch_page_async(session, url)
            soup = BeautifulSoup(page_content, 'lxml')

            tasks = []
            for article in soup.find_all('article'):
                title_tag = article.find('h2')
                if title_tag:
                    title = title_tag.get_text()

                    if self.keyword_match(title):
                        article_url = title_tag.find('a')['href']
                        full_article_url = urljoin(url, article_url)
                        tasks.append(self.parse_article_async(session, full_article_url, title))

            await asyncio.gather(*tasks)

    async def parse_article_async(self, session, full_article_url, title):
        """Асинхронный парсинг одной статьи с Habr."""
        article_content = await self.fetch_page_async(session, full_article_url)
        article_soup = BeautifulSoup(article_content, 'lxml')

        paragraphs = article_soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)
        demo = ' '.join(article_text.split()[:200])

        # Вывод результатов
        print(f'Название: {title}')
        print(f'URL: {full_article_url}')
        print(f'Демо-версия: {demo}\n')

    # Заглушки для других сайтов
    def parse_tproger(self):
        """Парсинг сайта tproger (логика будет добавлена позже)."""
        pass

    def parse_geekbrains(self):
        """Парсинг сайта geekbrains (логика будет добавлена позже)."""
        pass

    def parse_other_site(self):
        """Парсинг другого сайта (логика будет добавлена позже)."""
        pass

    def run(self):
        """Основная логика для запуска парсинга по списку сайтов."""
        for site in self.white_list:
            if 'habr.com' in site:
                self.parse_habr()  # Парсинг Habr
            elif 'tproger.ru' in site:
                self.parse_tproger()  # Парсинг tproger
            elif 'geekbrains.ru' in site:
                self.parse_geekbrains()  # Парсинг geekbrains
            else:
                self.parse_other_site()  # Парсинг другого сайта

# Пример использования
parser = Mighty_parser(white_list=['https://habr.com', 'https://tproger.ru'])
parser.run()
