from warnings import deprecated
import requests
from bs4 import BeautifulSoup
from google.cloud.exceptions import BadRequest
from requests import Response


class Scraper:

    BS_FEATURE_NAME = "html.parser"

    def scrap_fruits(self):
        url = "https://dietetycy.org.pl/owoce/"  # 50
        pass

    def scrap_vegetables(self):
        url = "https://dietetycy.org.pl/warzywa/"  # 50
        pass

    def scrap_animals(self):
        url = "https://all4mom.pl/lista-50-najpopularniejszych-zwierzat-domowych-oryginalni-pupile-dla-dzieci/"  # 50
        pass

    def scrap_colors(self):
        url = "https://preply.com/en/blog/red-is-the-new-black-let-s-learn-colors-and-shades-in-english/"  # 25
        pass

    def scrap_places_in_town(self):
        url = "http://www.grammar-monster.com/vocabulary/ESL-vocabulary-places-in-town.htm"  # 12
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.select("span.highlight")
            for row in rows:
                text = row.text.strip()
                if len(text) > 3:
                    words.add(text)
            return {"places_in_town": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")

    def scrap_jobs(self):
        url = "https://chatschool.pl/blog/zawody-po-angielsku/"  # 70
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all('b')
            for row in rows:
                text = row.text.strip()
                if 3 < len(text) < 15 and text.isalpha():
                    words.add(text)

            return {"jobs": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")


    def scrap_hobbies(self):
        url = "https://langeek.co/en/vocab/subcategory/800/word-list"  # 24
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all("div", class_="tw-text-sm sm:tw-text-lg tw-font-text-bold tw-block-1 tw-mb-3")
            for row in rows:
                text = row.text.strip()
                if len(text) > 3:
                    words.add(text)

            return {"hobbies": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")


    def scrap_drinks(self):
        url = "https://langeek.co/en/vocab/subcategory/146/word-list"  # 28
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all("div", class_="tw-text-sm sm:tw-text-lg tw-font-text-bold tw-block-1 tw-mb-3")
            for row in rows:
                text = row.text.strip()
                if len(text) > 3:
                    words.add(text)
            return {"drinks": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")


    def scarp_parts_of_house(self):
        url = "https://www.woodwardenglish.com/lesson/parts-of-the-house/"  # 22
        try:
            soup = self.__create_soup(url)
            words = list()
            rows = soup.find_all("li", class_="")
            for row in rows:
                text = row.text.strip()
                words.append(text)

            return {"partsOfHouse": words}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")


    def scrap_sports_words(self):
        url = "https://www.britannica.com/dictionary/eb/3000-words/topic/american-sports-vocabulary-english"  # 33
        try:
            soup = self.__create_soup(url)
            a_words_tags = soup.select('ul.t_words li a:not([target])')
            words = list()

            for a_word_tag in a_words_tags:
                text = a_word_tag.text
                bracket_pos = text.find("(")
                if bracket_pos != -1:
                    text = text[:bracket_pos]
                words.append(text.strip())

            return {"partsOfHouse": words}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")

    def scrap_music_instruments(self):
        url = "https://promova.com/english-vocabulary/music-instruments-in-english"  # 50
        return self.__promova_website_scraper("strong", "instruments", url)

    def scrap_technology(self):
        url = "https://promova.com/english-vocabulary/technology-vocabulary"
        return self.__promova_website_scraper("strong", "technology", url)


    def __promova_website_scraper(self, tag_name, category_name, promova_url):
        try:
            soup = self.__create_soup(promova_url)
            tags = soup.find_all(tag_name, class_="")
            words = list()
            for tag in tags:
                if len(tag.text.strip()) > 3:
                    text = tag.text.strip()
                    if text[-1] == ':':
                        text = text[:-1]
                    text = self.__clean_from_bracket_text(text)
                    words.append(text.strip())

            return {str(category_name): words}
        except BadRequest:
            print(f"cannot retrieve data from url {promova_url}")



    def __clean_from_bracket_text(self, tag_text):
        bracket_pos = tag_text.find("(")
        if bracket_pos != -1:
            return tag_text[:bracket_pos]
        return tag_text

    def __create_soup(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, self.BS_FEATURE_NAME)
        else:
            raise BadRequest("Status Code " + str(response.status_code))
