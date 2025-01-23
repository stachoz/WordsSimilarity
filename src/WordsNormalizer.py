import csv

class WordsNormalizer:

    accented_to_plain = {
        "a": ["ą", "à", "â", "ä", "á", "Á", "À", "Â", "Ä"],
        "c": ["ć", "č", "ç", "Ç", "Č"],
        "d": ["ď", "Ď"],
        "e": ["ę", "è", "é", "ê", "ë", "ě", "É", "È", "Ê", "Ë", "Ě"],
        "i": ["í", "î", "ï", "Í", "Î", "Ï"],
        "l": ["ł", "Ł"],
        "n": ["ń", "ñ", "ň", "Ñ", "Ň"],
        "o": ["ó", "ô", "ö", "Ó", "Ô", "Ö"],
        "r": ["ř", "Ř"],
        "s": ["ś", "š", "ß", "Ś", "Š"],
        "t": ["ť", "Ť"],
        "u": ["ù", "ú", "û", "ü", "ů", "Ú", "Û", "Ü", "Ů", "Ù"],
        "y": ["ý", "Ý"],
        "z": ["ź", "ž", "ż", "Ź", "Ž", "Ż"]
    }

    accent_map = {char: plain for plain, accented_chars in accented_to_plain.items() for char in accented_chars}


    def remove_accents(self, text):
        return ''.join(self.accent_map.get(char, char) for char in text)


    def normalize_csv(self, file_path, output_file):

        with open(file_path, mode='r', encoding='utf-8') as infile, \
                open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            writer.writeheader()

            for row in reader:
                normalized_row = {key: (self.remove_accents(value) if key != "category" else value)
                                  for key, value in row.items()}
                writer.writerow(normalized_row)

        print(f"Plik znormalizowany został zapisany jako: {output_file}")