import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors, cm

class WordsSimilarityGraph:

    def __init__(self, levenshtein_results_file):
        self.levenshtein_results_file = levenshtein_results_file
        self.output_dir = "graphs"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_graph_for_category(self, category):
        levenshtein_results = pd.read_csv(self.levenshtein_results_file)
        category_results = levenshtein_results[levenshtein_results['Kategoria'] == category]
        G = nx.Graph()
      
        
        for _, row in category_results.iterrows():
            language_1 = row['Język 1']
            language_2 = row['Język 2']
            avg_distance = row['Średnia odległość Levenshteina']

            # Add nodes and edges with weights representing the distance
            G.add_node(language_1)
            G.add_node(language_2)
            G.add_edge(language_1, language_2, weight=avg_distance)

        return G

    def create_average_graph(self):
        levenshtein_results = pd.read_csv(self.levenshtein_results_file)
        G = nx.Graph()

        
        grouped = levenshtein_results.groupby(['Język 1', 'Język 2'])['Średnia odległość Levenshteina'].mean().reset_index()

        for _, row in grouped.iterrows():
            language_1 = row['Język 1']
            language_2 = row['Język 2']
            avg_distance = row['Średnia odległość Levenshteina']

            
            G.add_node(language_1)
            G.add_node(language_2)
            G.add_edge(language_1, language_2, weight=avg_distance)

        return G

    def save_graph(self, G, category):
        pos = nx.kamada_kawai_layout(G)

        edges = G.edges(data=True)
        weights = [edge['weight'] for _, _, edge in edges]

        
        if len(weights) == 0:
            raise ValueError(f"No edges found for category {category}")
        if len(set(weights)) == 1:
            norm = colors.Normalize(vmin=weights[0] - 1, vmax=weights[0] + 1)
        else:
            norm = colors.Normalize(vmin=min(weights), vmax=max(weights))

        cmap = cm.get_cmap('RdYlGn')  # red to green colormap

        edge_colors = [cmap(norm(weight)) for weight in weights]

        fig, ax = plt.subplots(figsize=(12, 8))

        
        nx.draw(
            G, pos, with_labels=True, ax=ax,
            node_size=700,
            node_color='skyblue',
            font_size=10,
            font_color='black',
            edge_color=edge_colors,
            width=2
        )

        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        formatted_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_labels, font_size=8, ax=ax)
        ax.set_title(f"Lexical Proximity Between Languages - {category}", fontsize=16, pad=20)

         
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array(weights)  # Provide the data array for the colorbar
        cbar = fig.colorbar(sm, ax=ax, pad=0.1)
        cbar.set_label('Levenshtein Distance', fontsize=12)

        
        output_file = os.path.join(self.output_dir, f"{category}_graph.png")
        plt.savefig(output_file)
        plt.close()

    def generate_category_graphs(self):
        categories = [
            'places_in_town', 'jobs', 'hobbies', 'drinks', 'partsOfHouse',
            'instruments', 'technology', 'colors', 'animals', 'vegetables', 'fruits'
        ]

        
        for category in categories:
            print(f"Generating graph for category: {category}")
            G = self.create_graph_for_category(category)
            self.save_graph(G, category)

       

