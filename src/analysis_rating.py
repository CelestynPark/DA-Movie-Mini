import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import ast
from collections import Counter
from wordcloud import WordCloud

def load_processed_data(path='data/processed/merged_movies.csv'):
    return pd.read_csv(path)

def compute_weighted_rating(df, m_quantile=0.90):
    df = df.copy()
    C = df['vote_average'].mean()
    m = df['vote_count'].quantile(m_quantile)

    qualified = df[df['vote_count'] >= m].copy()
    qualified['weighted_rating'] = qualified.apply(
        lambda x: (x['vote_count'] / (x['vote_count'] + m)) * x['vote_average'] + (m / (m + x['vote_count'])) * C,
        axis=1
    )
    return qualified.sort_values('weighted_rating', ascending=False), C, m

def plot_top_rated_movies(df, top_n=15, output_dir='output/figures'):
    top_movies = df[['title', 'weighted_rating']].head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weighted_rating', y='title', data=top_movies, orient='h')
    plt.xlabel(f'Top {top_n} Movies (Weighted by Votes)')
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'top_weighted_movies.png'))
    plt.close()

def main():
    df = load_processed_data()
    top_df, C, m = compute_weighted_rating(df)
    plot_top_rated_movies(top_df)

    print(f"Rating analysis completed. Average vote (C) = {C:.2f}, min votes (m) = {m:.0f}")
    print("Top movies saved in output/figures/top_weighted_movies.png,")

if __name__ == '__main__':
    main()