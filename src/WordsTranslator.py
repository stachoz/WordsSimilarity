import pandas as pd
from google.cloud import translate_v2

class WordsTranslator:
    translate_client = translate_v2.Client()

    def translate(self, input_file, output_file):
        languages = ['fr', 'it', 'es', 'de', 'pl', 'cs']

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write('word,' + ','.join(languages) + ',category\n')

        words_data = pd.read_csv(input_file)

        for index, row in words_data.iterrows():
            word = row['word']
            category = row['category']
            translations = [word]

            for lang in languages:
                try:
                    translation = self.translate_client.translate(word, target_language=lang, source_language='en')['translatedText']

                    if '/' in translation:
                        translation = translation.split('/')[0]

                    translations.append(translation)
                except Exception as e:
                    print(f"Error translating '{word}' to {lang}: {e}")
                    continue

            translations.append(category)
            with open(output_file, 'a', encoding='utf-8') as f_out:
                f_out.write(','.join(translations) + '\n')


