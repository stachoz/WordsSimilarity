from src.WordsListScraper import Scraper
import csv
from src.WordsTranslator import WordsTranslator


def run_all_scrappers_and_save_to_file():
    scraper = Scraper()

    functions = [
        scraper.scrap_places_in_town,
        scraper.scrap_jobs,
        scraper.scrap_hobbies,
        scraper.scrap_drinks,
        scraper.scarp_parts_of_house,
        scraper.scrap_sports_words,
        scraper.scrap_music_instruments,
        scraper.scrap_technology,
        scraper.scrap_colors,
        scraper.scrap_animals,
        scraper.scrap_vegetables,
        scraper.scrap_fruits
    ]

    data = []

    for func in functions:
        result = func()  # Each function returns {"category": list(words)}
        for category, words_list in result.items():
            for word in words_list:
                data.append({"words": word, "category": category})

    with open("words_data.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["word", "category"])
        writer.writeheader()
        writer.writerows(data)

def main():
    t = WordsTranslator()
    t.translate()



if __name__ == '__main__':
    main()

