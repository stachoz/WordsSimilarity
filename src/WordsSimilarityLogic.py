from src.LanguageComparer import LanguageComparer
from src.WordsListScraper import Scraper
from src.WordsNormalizer import WordsNormalizer
from src.WordsTranslator import WordsTranslator
from src.WordsSimilarityGraph import WordsSimilarityGraph


class WordsSimilarityLogic:

    scraper_output_file = "words_data.csv"
    translator_output_file = "translated_words.csv"
    levenshtein_output_file = "levenshtein_results.csv"
    levenshtein_normalized_output_file = "levenshtein_normalized_results.csv"
    normalized_translated_words_output_file = "translated_words_normalized.csv"
    scraper = Scraper()
    translator = WordsTranslator()
    normalizer = WordsNormalizer()


    def run(self):
        """
            If translations and similarity measurements are already generated,
            comment out functions: scrap_all, translate and compute_average_distances.
        """
        self.scraper.scrap_all(output_file=self.scraper_output_file)
        self.translator.translate(input_file=self.scraper_output_file, output_file=self.translator_output_file)

        language_comparer = LanguageComparer(self.translator_output_file)
        result = language_comparer.compute_average_distances()
        language_comparer.save_results_to_csv(result, self.levenshtein_output_file)

        graph_generator = WordsSimilarityGraph(self.levenshtein_output_file)
        graph_generator.generate_category_graphs()
        average_graph = graph_generator.create_average_graph()
        graph_generator.save_graph(average_graph, "average_distances")


        self.normalizer.normalize_csv(self.translator_output_file, self.normalized_translated_words_output_file)

        language_comparer = LanguageComparer(self.normalized_translated_words_output_file)
        result = language_comparer.compute_average_distances()
        language_comparer.save_results_to_csv(result, self.levenshtein_normalized_output_file)

        graph_generator = WordsSimilarityGraph(self.levenshtein_normalized_output_file)
        average_graph = graph_generator.create_average_graph()
        graph_generator.save_graph(average_graph, "average_distances_normalized")


