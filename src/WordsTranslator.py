import pandas as pd
from translate import Translator


class WordsTranslator:

    def translate(self):
        input_file = 'words_data.csv'
        output_file = 'translated_words.csv'

        languages = ['fr', 'it', 'es', 'de', 'pl', 'cs']

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write('words,' + ','.join(languages) + ',category\n')

        words_data = pd.read_csv(input_file)

        for index, row in words_data.iterrows():
            word = row['word']
            category = row['category']
            translations = [word]

            for lang in languages:
                try:
                    translator = Translator(provider='mymemory', from_lang='en', to_lang=lang)
                    translation = translator.translate(word)
                    translations.append(translation)
                except Exception as e:
                    translations.append('')  # W przypadku błędu dodajemy pustą wartość
                    print(f"Error translating '{word}' to {lang}: {e}")

            translations.append(category)
            with open(output_file, 'a', encoding='utf-8') as f_out:
                f_out.write(','.join(translations) + '\n')

        print(f"Tłumaczenie zakończone. Wyniki zapisano w pliku: {output_file}")



