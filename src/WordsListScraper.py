import requests
from bs4 import BeautifulSoup
from google.cloud.exceptions import BadRequest
from requests import Response


class Scraper:

    def scrap_fruits(self):
        url = "https://dietetycy.org.pl/owoce/"
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all("h3", class_="wp-block-heading")

            for row in rows:
                strong_tag = row.find("strong")
                if strong_tag:
                    text = strong_tag.text.strip()
                    if text.isalpha() and len(text) > 2:
                        words.add(text)

            return {"fruits": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")


    def scrap_vegetables(self):
        url = "https://dietetycy.org.pl/warzywa/"
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all("h3", class_="wp-block-heading")

            for row in rows:
                strong_tag = row.find("strong")
                if strong_tag:
                    text = strong_tag.text.strip()
                    if text.isalpha() and len(text) > 2:
                        words.add(text)

            return {"vegetables": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")

    def scrap_animals(self):
        url = "https://all4mom.pl/lista-50-najpopularniejszych-zwierzat-domowych-oryginalni-pupile-dla-dzieci/"
        try:
            soup = self.__create_soup(url)
            words = set()
            rows = soup.find_all("span", style="font-size: 18pt;")

            for row in rows:
                text = row.text.strip()
                animal_name = text.split(". ", 1)[-1]
                if animal_name.isalpha() and len(animal_name) > 2:
                    words.add(animal_name)

            return {"animals": list(words)}
        except BadRequest:
            print(f"cannot retrieve data from url {url}")

    def scrap_colors(self):
        url = "https://preply.com/en/blog/red-is-the-new-black-let-s-learn-colors-and-shades-in-english/"
        try:
            soup = self.__create_soup(url)
            colors = set()

            rows = soup.select("#preply_post li")

            for row in rows:
                text = row.text.strip()
                color_name = text.split("[")[0].strip()
                colors.add(color_name)

            return {"colors": list(colors)}

        except BadRequest:
            print(f"cannot retrieve data from url {url}")

    def scrap_places_in_town(self):
        url = "http://www.grammar-monster.com/vocabulary/ESL-vocabulary-places-in-town.htm"
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
        url = "https://chatschool.pl/blog/zawody-po-angielsku/"
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
        url = "https://langeek.co/en/vocab/subcategory/800/word-list"
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
        url = "https://langeek.co/en/vocab/subcategory/146/word-list"
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
        url = "https://www.woodwardenglish.com/lesson/parts-of-the-house/"
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
        url = "https://www.britannica.com/dictionary/eb/3000-words/topic/american-sports-vocabulary-english"
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
        url = "https://promova.com/english-vocabulary/music-instruments-in-english"
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
            return BeautifulSoup(response.text, "html.parser")
        else:
            raise BadRequest("Status Code " + str(response.status_code))
