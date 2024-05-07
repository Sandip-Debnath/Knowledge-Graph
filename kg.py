import re
import pandas as pd
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

# Load the English language model for spaCy
nlp = spacy.load('en_core_web_sm')

def extract_relationships(sentence):
    relationships = []
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'ROOT':  # Check if token is the root of the sentence
            verb = token.lemma_
            subject = None
            obj = None  # Initialize object to None
            for child in token.children:
                if child.dep_ == 'nsubj':  # Check if the child is a subject
                    subject = child.text
                elif child.dep_ == 'dobj':  # Check if the child is a direct object
                    obj = child.text
            if subject is not None and obj is not None:  # Check if subject and obj are not None
                relationships.append((verb, subject, obj))
    return relationships

# List of CSV files (update these filenames accordingly)
csv_files = ['burning.csv', 'antimortem.csv', 'throtlling.csv', 'suicidalpoisoning.csv']

# Iterate over each CSV file
for csv_file in csv_files:
    # Read the CSV file containing paragraphs
    df = pd.read_csv(csv_file, encoding='latin1')

    # Create a directed graph
    G = nx.DiGraph()

    # Iterate over each paragraph in the DataFrame
    for paragraph in tqdm(df['paragraphs']):
        # Split the paragraph into sentences
        sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)

        # Extract relationships from each sentence
        for sentence in sentences:
            extracted_relationships = extract_relationships(sentence)
            for verb, subject, obj in extracted_relationships:
                G.add_edge(subject, obj, label=verb)

    # Draw the graph with customized appearance
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, seed=42, k=2.5)  # Adjust k value for sparser layout
    nx.draw(G, pos,
            with_labels=True,
            node_size=3000,
            node_color='skyblue',
            font_size=12,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            node_shape='o')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title(f'Knowledge Graph: {csv_file}')
    plt.show()
