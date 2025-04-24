import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def load_processed_data(path='data/processed/merged_movies.csv'):
    return pd.read_csv(path)

def explode_genres(df):
    df = df.copy()
    df['genres'] = df['genres'].fillna('[]').apply(eval)
    df_exploded = df.explode('genres')
    df_exploded = df_exploded[df_exploded['genres'].notnull() & (df_exploded['genres'] != '')]
    return df_exploded

def genre_avg_ratings(df):
    result = df.groupby('genres')['vote_average'].mean().sort_values(ascending=False)
    return result

def genre_movie_counts(df):
    return df['genres'].value_counts()

def plot_genre_boxplot(df, output_dir='output/figures'):
    df_box = df[['genres', 'vote_average']].dropna()
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='genres', y='vote_average', data=df_box)
    plt.xticks(rotation=45, ha='right')
    plt.title('Genre-wise Vote Average Distribution')
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'genre_boxplot.png'))
    plt.close()

def plot_genre_avg_bar(avg_rating_series, output_dir='output/figures'):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_rating_series.values, y=avg_rating_series.index, orient='h')
    plt.title('Average Vote by Genre')
    plt.xlabel('Average Rating')
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'genre_avg_rating.png'))
    plt.close()

def main():
    df = load_processed_data()
    df = explode_genres(df)

    avg_rating = genre_avg_ratings(df)
    plot_genre_avg_bar(avg_rating)
    
    plot_genre_boxplot(df)

    print("Genre analysis completed. Visualizations saved in output/figures,")

if __name__ == '__main__':
    main()