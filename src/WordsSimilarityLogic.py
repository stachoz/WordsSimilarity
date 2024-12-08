from src.LanguageComparer import LanguageComparer
from src.WordsListScraper import Scraper
from src.WordsTranslator import WordsTranslator


class WordsSimilarityLogic:

    scraper_output_file = "words_data.csv"
    translator_output_file = "translated_words.csv"
    scraper = Scraper()
    translator = WordsTranslator()


    def run(self):
        """
            If translations and similarity measurements are already generated,
            comment out functions: scrap_all, translate and compute_average_distances.
        """
        self.scraper.scrap_all(output_file=self.scraper_output_file)
        self.translator.translate(input_file=self.scraper_output_file, output_file=self.translator_output_file)

        language_comparer = LanguageComparer(self.translator_output_file, 7)
        result = language_comparer.compute_average_distances()
        language_comparer.save_results_to_csv("levenshtein.csv", result)
