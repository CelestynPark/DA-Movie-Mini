import pandas as pd
import numpy as np
import os
import ast

def load_raw_data(raw_dir):
    movies = pd.read_csv(os.path.join(raw_dir, 'movies_metadata.csv'), low_memory=False)
    credits = pd.read_csv(os.path.join(raw_dir, 'credits.csv'))
    keywords = pd.read_csv(os.path.join(raw_dir, 'keywords.csv'))
    links = pd.read_csv(os.path.join(raw_dir, 'links.csv'))
    return movies, credits, keywords, links

def clean_movies_metadata(df):
    df = df.copy()

    df = df[df['id'].apply(lambda x: str(x).isdigit())]
    df['id'] = df['id'].astype(int)

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year

    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')

    df['genres'] = df['genres'].apply(parse_json_list)

    return df

def parse_json_list(text):
    try:
        data = ast.literal_eval(text)
        if isinstance(data, list):
            return [d['name'] for d in data if 'name' in d]
        return []
    except (ValueError, SyntaxError):
        return []
    
def merge_all(movies, credits, keywords, links):
    credits['id'] = credits['id'].astype(int)
    keywords['id'] = keywords['id'].astype(int)
    links = links[links['tmdbId'].notnull()].copy()
    links['tmdbId'] = links['tmdbId'].astype(int)

    df = movies.merge(credits, on='id', how='left')
    df = df.merge(credits, on='id', how='left')
    df = df.merge(links, left_on='id', right_on='tmdbId', how='left')

    return df

def save_processed_data(df, out_path):
    df.to_csv(out_path, index=False)

def main():
    raw_dir = "data/raw"
    output_file = 'data/processed/merged_movies.csv'

    movies, credits, keywords, links = load_raw_data(raw_dir)
    movies = clean_movies_metadata(movies)
    df = merge_all(movies, credits, keywords, links)
    save_processed_data(df, output_file)

    print(f"Saved cleaned and merged data to {output_file}")

if __name__ == '__main__':
    main()