import csv
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed


class Translator:

    def __init__(self, target_languages: list, words: list):
        self.target_languages = target_languages
        self.words = words

    def translate_words(self, target_language):
        try:
            translator = GoogleTranslator(source="en", target=target_language)
            translated_words = [translator.translate(word) for word in self.words]
            return target_language, translated_words
        except Exception as e:
            print(f"Error during translation to language {target_language}: {e}")
            return target_language, []

    def translate_and_save_to_csv(self, output_file = "words.csv"):

        translations = {}

        with ThreadPoolExecutor(max_workers=len(self.target_languages)) as executor:
            futures = {executor.submit(self.translate_words,lang): lang for lang in self.target_languages}
            for future in as_completed(futures):
                lang, translated_words = future.result()
                translations[lang] = translated_words

        self.save_to_csv(translations, output_file)

    def save_to_csv(self, words, output_file):
        languages = list(words.keys())
        words_count = len(self.words)
        print(words_count)

        with open(output_file, "w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Word"] + languages)

            for i in range(words_count):
                row = [self.words[i]]
                row += [words[lang][i] for lang in languages]
                writer.writerow(row)
