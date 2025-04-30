import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import ast
from collections import Counter
from wordcloud import WordCloud

def load_processed_data(path='data/processed/merged_movies.csv'):
    return pd.read_csv(path)

def extract_keywords(df):
    all_keywords = []
    for kw_str in df["keywords"]:
        try:
            kws = ast.literal_eval(kw_str)
            all_keywords.extend([k['name'] for k in kws if 'name' in k])
        except:
            continue
    return all_keywords

def count_keywords(keywords_list):
    return Counter(keywords_list)

def plot_top_keywords(keyword_counter, top_n=30, output_dir='output/figures'):
    top_keywords = keyword_counter.most_common(top_n)
    words, counts = zip(*top_keywords)
    plt.figure(figsize=(10, 8))
    plt.barh(words[::-1], counts[::-1])
    plt.title(f"Top {top_n} Keywords")
    plt.xlabel("Count")
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'top_keywords.png'))
    plt.close()

def generate_wordcloud(keyword_counter, output_dir='output/figures'):
    wc = WordCloud(width=1000, height=600, background_color='white')
    wc.generate_from_frequencies(keyword_counter)
    os.makedirs(output_dir, exist_ok=True)
    wc.to_file(os.path.join(output_dir, 'keyword_wordcloud.png'))

def main():
    df = load_processed_data()
    keywords_list = extract_keywords(df)
    keyword_counter = count_keywords(keywords_list)

    plot_top_keywords(keyword_counter)
    generate_wordcloud(keyword_counter)

    print("Keyword analysis completed. Visualizations saved in output/figures,")

if __name__ == '__main__':
    main()