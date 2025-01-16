from src.LanguageComparer import LanguageComparer
from src.WordsListScraper import Scraper
from src.WordsTranslator import WordsTranslator
from src.WordsSimilarityGraph import WordsSimilarityGraph


class WordsSimilarityLogic:

     def run(self):
        graph_generator = WordsSimilarityGraph("data/levenshtein_results.csv")

        
        print("Generating graphs for all categories...")
        graph_generator.generate_category_graphs()  

        
        print("Generating graph for average distances")
        average_graph = graph_generator.create_average_graph()  
        graph_generator.save_graph(average_graph, "average_distances")  

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
        language_comparer.save_results_to_csv("levenshtein.csv", result)
