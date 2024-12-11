import csv


class LanguageComparer:
    def __init__(self, filename):
        self.filename = filename
        self.language_names = ['Angielski', 'Francuski', 'Wloski', 'Hiszpanski', 'Niemiecki', 'Polski', 'Czeski']
        self.num_translations = len(self.language_names)
        self.data = []
        self.categories = {}

    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                translations = row[:self.num_translations]
                category = row[self.num_translations]
                self.data.append((translations, category))
                if category not in self.categories:
                    self.categories[category] = []
                self.categories[category].append(translations)

    # Implementacja algorytmu Levenshteina
    def levenshtein_distance(self, s1, s2):
        if len(s1) == 0:
            return len(s2)
        if len(s2) == 0:
            return len(s1)

        rows = len(s1) + 1
        cols = len(s2) + 1
        distance_matrix = [[0 for x in range(cols)] for x in range(rows)]

        for i in range(1, rows):
            distance_matrix[i][0] = i
        for j in range(1, cols):
            distance_matrix[0][j] = j

        for i in range(1, rows):
            for j in range(1, cols):
                if s1[i - 1] == s2[j - 1]:
                    cost = 0
                else:
                    cost = 1
                distance_matrix[i][j] = min(
                    distance_matrix[i - 1][j] + 1,
                    distance_matrix[i][j - 1] + 1,
                    distance_matrix[i - 1][j - 1] + cost
                )

        return distance_matrix[rows - 1][cols - 1]

    def compute_average_distances(self):
        self.load_data()
        results = {}
        for category, translations_list in self.categories.items():
            distances = {}
            counts = {}
            for i in range(self.num_translations):
                for j in range(i + 1, self.num_translations):
                    key = (i, j)
                    distances[key] = 0
                    counts[key] = 0

            for translations in translations_list:
                for i in range(self.num_translations):
                    for j in range(i + 1, self.num_translations):
                        dist = self.levenshtein_distance(translations[i], translations[j])
                        key = (i, j)
                        distances[key] += dist
                        counts[key] += 1

            average_distances = {}
            for key in distances:
                if counts[key] > 0:
                    average = distances[key] / counts[key]
                else:
                    average = 0
                average_distances[key] = average

            results[category] = average_distances

        return results

    def save_results_to_csv(self, results, output_filename):
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            header = ['Kategoria', 'Język 1', 'Język 2', 'Średnia odległość Levenshteina']
            writer.writerow(header)
            for category, averages in results.items():
                for (i, j), average in averages.items():
                    lang_i = self.language_names[i] if i < len(self.language_names) else f'Język {i + 1}'
                    lang_j = self.language_names[j] if j < len(self.language_names) else f'Język {j + 1}'
                    writer.writerow([category, lang_i, lang_j, f"{average:.2f}"])
