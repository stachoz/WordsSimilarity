from src.LanguageComparer import LanguageComparer
from src.WordsListScraper import Scraper
from src.WordsTranslator import WordsTranslator
from src.WordsSimilarityGraph import WordsSimilarityGraph


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

        language_comparer = LanguageComparer(self.translator_output_file)
        result = language_comparer.compute_average_distances()
        language_comparer.save_results_to_csv(result, "levenshtein.csv")
         
        graph_generator = WordsSimilarityGraph("levenshtein_results.csv")
        graph_generator.generate_category_graphs() 
        average_graph = graph_generator.create_average_graph()  
        graph_generator.save_graph(average_graph, "average_distances") 
