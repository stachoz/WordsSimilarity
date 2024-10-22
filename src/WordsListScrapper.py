import requests
from bs4 import BeautifulSoup
from requests import Response


class WebPageFetcher:
    def __init__(self, url):
        self.url = url
        self.html_content = None


    def getScrappedWords(self) -> set:
        wordsList = self.fetch_html()
        return self.clean_words_list(wordsList)

    def fetch_html(self) -> list:
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return self.clean_words_list(self.scrapp_words(response))
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return []

    def scrapp_words(self, response: Response) -> list:
        soup = BeautifulSoup(response.text, 'html.parser')
        words = []
        rows = soup.find_all('tr')
        for row in rows:
            a_tag = row.find('a')
            if(a_tag):
                words.append(a_tag.text)

        return words

    def clean_words_list(self, words: list) -> set:
        for word in words:
            if(len(word) < 3):
                words.remove(word)

        return set(words)
