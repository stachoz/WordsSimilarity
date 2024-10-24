import requests
from bs4 import BeautifulSoup
from requests import Response


class WebPageFetcher:
    def __init__(self, url):
        self.url = url
        self.html_content = None

    def get_scrapped_words(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return self.scrapp_words(response)
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return []

    def scrapp_words(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        words = set()
        rows = soup.find_all('tr')
        for row in rows:
            a_tag = row.find('a')
            if(a_tag and len(a_tag.text) > 3):
                words.add(a_tag.text)
        return list(words)