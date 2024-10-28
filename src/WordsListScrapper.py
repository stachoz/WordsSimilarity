from warnings import deprecated

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

    @deprecated
    def scrapp_words(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        words = set()
        rows = soup.find_all('tr')
        for row in rows:
            a_tag = row.find('a')
            if(a_tag and len(a_tag.text) > 3):
                words.add(a_tag.text)
        return list(words)

    def scrapp_fruits(self):
        url = "https://dietetycy.org.pl/owoce/" # 50
        pass

    def scrapp_vegetables(self):
        url = "https://dietetycy.org.pl/warzywa/" # 50
        pass

    def scrapp_animals(self):
        url = "https://all4mom.pl/lista-50-najpopularniejszych-zwierzat-domowych-oryginalni-pupile-dla-dzieci/" # 50
        pass

    def scrapp_colors(self):
        url = "https://preply.com/en/blog/red-is-the-new-black-let-s-learn-colors-and-shades-in-english/" # 25
        pass

    def scrapp_places_in_town(self):
        url = "http://www.grammar-monster.com/vocabulary/ESL-vocabulary-places-in-town.htm" # 12
        pass

    def scrapp_jobs(self):
        url = "https://chatschool.pl/blog/zawody-po-angielsku/"  # 70
        pass

    def scrapp_hobbies(self):
        url = "https://langeek.co/en/vocab/subcategory/800/word-list" # 24
        pass

    def scrapp_drinks(self):
        url = "https://langeek.co/en/vocab/subcategory/146/word-list" # 28
        pass

    def scarpp_parts_of_house(self):
        url = "https://www.woodwardenglish.com/lesson/parts-of-the-house/" # 22
        pass

    def scrapp_sports_words(self):
        # TODO clean words from text inside ()
        url = "https://www.britannica.com/dictionary/eb/3000-words/topic/american-sports-vocabulary-english" # 33
        pass

    def scrapp_music_instruments(self):
        url = "https://promova.com/english-vocabulary/music-instruments-in-english" # 50
        pass

    def scrapp_technology(self):
        url = "https://www.learnenglish.com/vocabulary/technology/learn-technology-vocabulary-in-english/" # 100
        pass

    
