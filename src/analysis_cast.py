import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import ast

def load_processed_data(path='data/processed/merged_movies.csv'):
    return pd.read_csv(path)

def parse_json_cast_column(column):
    return column.fillna('[]').apply(lambda x: [d['name'] for d in ast.literal_eval(x) if 'name' in d] if isinstance(x, str) else [])

def parse_json_crew_column(column, job='Director'):
    return column.fillna('[]').apply(
        lambda x: [d['name'] for d in ast.literal_eval(x) if 'name' in d and d.get('job') == job] if isinstance(x, str) else []
    )

def extract_top_directors(df, top_n=10):
    director_votes = {}
    for crew_list, vote in zip(df['crew_x'], df['vote_average']):
        try:
            crew = ast.literal_eval(crew_list)
            for member in crew:
                if member.get('job') == 'Director':
                    name = member['name']
                    if name in director_votes:
                        director_votes[name].append(vote)
                    else:
                        director_votes[name] = [vote]
        except:
            continue

    director_avg = {k: sum(v)/len(v) for k, v in director_votes.items() if len(v) >= 3}
    return sorted(director_avg.items(), key=lambda x: x[1], reverse=True)[:top_n]

def extract_top_actors(df, top_n=20):
    actor_freq = {}
    for cast_list in df['cast_x']:
        try:
            cast = ast.literal_eval(cast_list)
            for member in cast:
                name = member['name']
                if name:
                    actor_freq[name] = actor_freq.get(name, 0) + 1
        except:
            continue

    return sorted(actor_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

def plot_top_directors(director_list, output_dir='output/figures'):
    names, scores = zip(*director_list)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=scores, y=names, orient='h')
    plt.xlabel('Average Rating')
    plt.title('Top Directors by Average Rating (min 3 films)')
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'top_directors.png'))
    plt.close()
    
def plot_top_actors(actor_list, output_dir='output/figures'):
    names, counts = zip(*actor_list)
    plt.figure(figsize=(10, 8))
    sns.barplot(x=counts, y=names, orient='h')
    plt.xlabel('Number of Appearances')
    plt.title('Top Appearing Actors')
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'top_actors.png'))
    plt.close()

def main():
    df = load_processed_data()
    top_directors = extract_top_directors(df)
    plot_top_directors(top_directors)
    
    top_actors = extract_top_actors(df)
    plot_top_actors(top_actors)

    print("Cast & Director analysis completed. Visualizations saved in output/figures,")

if __name__ == '__main__':
    main()