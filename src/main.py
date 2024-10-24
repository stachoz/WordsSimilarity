import WordsListScrapper
import Translator

def main():
    url = "http://pl.talkenglish.com/vocabulary/top-500-adjectives.aspx"

    scrapper = WordsListScrapper.WebPageFetcher(url)
    words = scrapper.get_scrapped_words()
    # polish french germany italian portuguese, words size is ~500
    translator = Translator.Translator(["pl", "fr", "de"], words[:10])

    translator.translate_and_save_to_csv()





if __name__ == '__main__':
    main()

