import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

whitelist = [
    'https://habr.com',
    'https://tproger.ru'
]

keywords = ['Python', 'Django', 'парсинг', 'Питон', 'Джанго']


def parse_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for the articles differently depending on site structure
    for article in soup.find_all('h2'):
        title = article.get_text()
        if any(keyword.lower() in title.lower() for keyword in keywords):
            # Check parent tag for article content
            article_parent = article.find_parent('article') or article.find_parent(
                'div')  # Try div if article not found
            if article_parent:
                paragraphs = article_parent.find_all('p')  # Find all paragraph tags
                if not paragraphs:
                    paragraphs = article_parent.find_all('div')  # If no <p>, try <div> as fallback

                article_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
                demo = ' '.join(article_text.split()[:200])  # Limit the text to 200 words for demo

                # Extract the article URL
                article_url = article.find('a')['href'] if article.find('a') else url
                article_url = urljoin(url, article_url)  # Ensure the URL is absolute

                print(f'Найдена статья: {title} на {article_url}')
                print(f'title: {title}, demo: {demo}\n')


for site in whitelist:
    parse_site(site)