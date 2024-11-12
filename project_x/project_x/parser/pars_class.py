from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
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
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return any(keyword.lower() in title.lower() for keyword in self.keywords)

    async def fetch_page_async(self, session, url):
        """Асинхронная загрузка страницы."""
        async with session.get(url) as response:
            return await response.text()

    async def parse_habr_async(self):
        """Асинхронный парсинг статей с сайта Habr с пагинацией."""
        base_url = 'https://habr.com/ru/all/'
        matched_articles = 0
        page_number = 1

        async with aiohttp.ClientSession() as session:
            while matched_articles < 10:  # Требуется получить хотя бы 10 подходящих статей
                # Формируем URL для каждой страницы
                paginated_url = f'{base_url}page{page_number}/'
                page_content = await self.fetch_page_async(session, paginated_url)
                soup = BeautifulSoup(page_content, 'lxml')

                tasks = []
                for article in soup.find_all('article'):
                    title_tag = article.find('h2')
                    if title_tag:
                        title = title_tag.get_text()

                        if self.keyword_match(title):
                            article_url = title_tag.find('a')['href']
                            full_article_url = urljoin(base_url, article_url)
                            tasks.append(self.parse_article_async(session, full_article_url, title))
                            matched_articles += 1
                            if matched_articles >= 5:
                                break

                # Выполняем задачи для всех найденных статей на странице
                await asyncio.gather(*tasks)
                page_number += 1

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
    def scroll_and_load(self, url, scroll_limit=5):
        """Прокручиваем страницу и подгружаем статьи."""
        driver = webdriver.Chrome()  # Укажите путь к драйверу, если он не в PATH
        driver.get(url)
        time.sleep(3)  # Ждем загрузки страницы

        # Прокручиваем страницу, чтобы подгрузить больше статей
        for _ in range(scroll_limit):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Ждем подгрузки контента

        # Получаем HTML содержимое после прокрутки
        page_content = driver.page_source
        driver.quit()
        return page_content

    async def parse_itproger_async(self):
        """Асинхронный парсинг всех статей с сайта ITProger."""
        url = 'https://tproger.ru/news'
        page_content = self.scroll_and_load(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        matched_articles = 0
        async with aiohttp.ClientSession() as session:
            tasks = []
            for article in soup.find_all('article', class_='tp-ui-post-card'):
                title_tag = article.find('h2', class_='tp-ui-post-card__title')
                link_tag = title_tag.find('a', class_='tp-ui-post-card__link') if title_tag else None

                if link_tag:
                    title = link_tag.get_text()
                    if self.keyword_match(title):
                        article_url = link_tag['href']
                        full_article_url = urljoin(url, article_url)
                        tasks.append(self.parse_article_async(session, full_article_url, title))
                        matched_articles += 1
                        if matched_articles >= 10:
                            break

            await asyncio.gather(*tasks)

    async def parse_article_async(self, session, full_article_url, title):
        """Асинхронный парсинг отдельной статьи с TProger."""
        article_content = await self.fetch_page_async(session, full_article_url)
        article_soup = BeautifulSoup(article_content, 'html.parser')

        paragraphs = article_soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)
        demo = ' '.join(article_text.split()[:200])

        # Вывод результатов
        print(f'Название: {title}')
        print(f'URL: {full_article_url}')
        print(f'Демо-версия: {demo}\n')
    async def run(self):
        """Основная логика для запуска парсинга по списку сайтов."""
        for site in self.white_list:
            if 'habr.com' in site:
                await self.parse_habr_async()  # Парсинг Habr
            elif 'tproger.ru' in site:
                await self.parse_itproger_async()  # Парсинг tproger

# Пример использования
if __name__ == "__main__":
    parser = Mighty_parser(white_list=['https://tproger.ru'])#, 'https://habr.com'])
    asyncio.run(parser.run())  # Запуск асинхронного парсинга

