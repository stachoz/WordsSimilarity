from src.LanguageComparer import LanguageComparer


def test():
    comparer = LanguageComparer('translated_words.csv', 7)
    result = comparer.compute_average_distances()

    # Zapisanie wyników do pliku CSV
    output_filename = 'wyniki_levenshtein.csv'
    comparer.save_results_to_csv(result, output_filename)
    print(f"Wyniki zostały zapisane do pliku {output_filename}")


if __name__ == '__main__':
    test()
