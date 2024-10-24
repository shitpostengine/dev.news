from django.db import models
import requests
from bs4 import BeautifulSoup

class Worker(models.Model):
    name = models.CharField(max_length=25, blank=False)
    mail = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.name

class Parser():
    whitelist = [
        'https://habr.com',
        'https://tproger.ru'
    ]
    keywords = ['Python', 'Django', 'парсинг']

    def parse_site(url, keywords):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.find_all('h2'):  # Пример для заголовков
            title = article.get_text()
            if any(keyword.lower() in title.lower() for keyword in keywords):
                print(f'Найдена статья: {title} на {url}')

    for site in whitelist:
        parse_site(site, keywords)
