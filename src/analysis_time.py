import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def load_processed_data(path='data/processed/merged_movies.csv'):
    return pd.read_csv(path)

def count_movies_per_year(df):
    return df.groupby('release_year').size()

def average_rating_per_year(df):
    return df.groupby('release_year')['vote_average'].mean()

def average_popularity_per_year(df):
    return df.groupby('release_year')['popularity'].mean()

def plot_time_series(series, title, ylabel, filename, output_dir='output/figures'):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=series.index, y=series.values)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def main():
    df = load_processed_data()
    
    df = df[df['release_year'].notna()]
    df['release_year'] = df['release_year'].astype(int)
    df = df[(df['release_year'] >= 1900) & (df['release_year'] <= 2025)]

    count_series = count_movies_per_year(df)
    avg_rating_series = average_rating_per_year(df)
    avg_popularity_series = average_popularity_per_year(df)

    plot_time_series(count_series, 'Number of Movies Released per Year', 'Count', 'yearly_movie_count.png')
    plot_time_series(avg_rating_series, 'Average Rating per Year', 'Average Rating', 'yearly_avg_rating.png')
    plot_time_series(avg_popularity_series, 'Average Popularity per Year', 'Average Popularity', 'yearly_avg_popularity.png')
    
    print("Time-based analysis completed. Visualizations saved in output/figures,")

if __name__ == '__main__':
    main()