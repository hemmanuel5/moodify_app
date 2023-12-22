import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy

# Set up Spotify API credentials
client_id = 'your-client-id'
client_secret = 'your-client-secret'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

train_data = pd.read_csv('/Users/hemmanuel/Downloads/training_data(2).csv')
test_data = pd.read_csv('/Users/hemmanuel/Downloads/data 2.csv')

moods = [
    "Excited",
    "Happy",
    "Calm",
    "Tired",
    "Bored",
    "Sad",
    "Nervous",
    "Angry",
    "Stressed",
]

def calculate_mood_score(train_data):
# Check if 'time_signature' is in the DataFrame
    if 'time_signature' not in train_data.columns:
        # Redistribute weights for the available features
        weights = {
            'energy': 0.175,
            'acousticness': 0.115,
            'valence': 0.23,
            'instrumentalness': 0.115,
            'speechiness': 0.115,
            'danceability': 0.175,
            'liveness': 0.058,
            'mode': 0.058,
            'loudness': 0.115,
            'key': 0.115,
            'tempo': 0.115
        }
    else:
        # Use the original weights
        weights = {
            'energy': 0.15,
            'acousticness': 0.1,
            'valence': 0.2,
            'instrumentalness': 0.1,
            'speechiness': 0.1,
            'danceability': 0.15,
            'liveness': 0.05,
            'mode': 0.05,
            'loudness': 0.1,
            'time_signature': 0.05,
            'key': 0.05,
            'tempo': 0.1
        }

    numeric_columns = ['energy', 'acousticness', 'valence', 'instrumentalness', 'speechiness',
                       'danceability', 'liveness', 'mode', 'loudness', 'key', 'tempo']

    train_data[numeric_columns] = train_data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    #mood_score formula created by chatgpt
    mood_score = train_data[weights.keys()].dot(pd.Series(weights))

    # Most of the mood conditions created by chatgpt
    neutral_threshold = 0.1  # Adjust as needed
    neutral_condition = (mood_score > -neutral_threshold) & (mood_score < neutral_threshold)
    neutral_condition = neutral_condition & (train_data['acousticness'] > 0.4) & (train_data['valence'] > 0.3)  # Adjust as needed

    excited_condition = mood_score > 0.7
    happy_condition = (mood_score > 0.5) & (train_data['energy'] > 0.5) & (train_data['valence'] > 0.4) & (train_data['danceability'] > 0.4)
    calm_condition = (train_data['energy'] < 0.5) & (train_data['valence'] > 0.4) & (train_data['acousticness'] > 0.5) & (train_data['loudness'] < -15)
    tired_condition = (train_data['energy'] < 0.4) & (train_data['valence'] < 0.5) & (train_data['loudness'] < -10) & (train_data['tempo'] < 100)
    bored_condition = (train_data['energy'] < 0.5) & (train_data['valence'] < 0.5) & (train_data['danceability'] < 0.5) & (train_data['tempo'] < 110)
    sad_condition = (mood_score < 0.3) & (train_data['energy'] < 0.6) & (train_data['valence'] < 0.6) & (train_data['acousticness'] > 0.4)
    nervous_condition = (mood_score > 0.4) & (train_data['energy'] > 0.5) & (train_data['valence'] < 0.6) & (train_data['loudness'] > -15)
    angry_condition = (mood_score > 0.5) & (train_data['energy'] > 0.6) & (train_data['valence'] < 0.5) & (train_data['loudness'] > -12)
    stressed_condition = (mood_score > 0.4) & (train_data['energy'] > 0.5) & (train_data['valence'] < 0.6) & (train_data['loudness'] > -10) & (train_data['speechiness'] > 0.2)

    train_data['mood'] = 'Neutral'

    train_data.loc[excited_condition, 'mood'] = 'Excited'
    train_data.loc[happy_condition, 'mood'] = 'Happy'
    train_data.loc[sad_condition, 'mood'] = 'Sad'
    train_data.loc[calm_condition, 'mood'] = 'Calm'
    train_data.loc[tired_condition, 'mood'] = 'Tired'
    train_data.loc[bored_condition, 'mood'] = 'Bored'
    train_data.loc[nervous_condition, 'mood'] = 'Nervous'
    train_data.loc[angry_condition, 'mood'] = 'Angry'
    train_data.loc[stressed_condition, 'mood'] = 'Stressed'

    # Define mood conditions based on valence and energy
    high_energy_high_valence_condition = (train_data['energy'] > 0.7) & (train_data['valence'] > 0.7)
    high_energy_low_valence_condition = (train_data['energy'] > 0.7) & (train_data['valence'] < 0.3)
    low_energy_high_valence_condition = (train_data['energy'] < 0.3) & (train_data['valence'] > 0.7)
    low_energy_low_valence_condition = (train_data['energy'] < 0.3) & (train_data['valence'] < 0.3)

    # Assign specific mood labels based on valence and energy conditions
    train_data.loc[high_energy_high_valence_condition, 'mood'] = 'Excited'
    train_data.loc[high_energy_low_valence_condition, 'mood'] = 'Angry'
    train_data.loc[low_energy_high_valence_condition, 'mood'] = 'Calm'
    train_data.loc[low_energy_low_valence_condition, 'mood'] = 'Sad'

# Map specific genres to moods based on the defined conditions
    if 'track_genre' in train_data.columns:
        genre_mood_mapping = {
            'chill': 'Calm',
            'classical': 'Calm',
            'disco': 'Excited',
            'electronic': 'Excited',
            'folk': 'Calm',
            'hip-hop': 'Excited',
            'indie': 'Neutral',
            'jazz': 'Calm',
            'metal': 'Angry',
            'pop': 'Happy',
            'reggae': 'Happy',
            'salsa': 'Happy',
            'samba': 'Happy',
            'sleep': 'Tired',
            'soul': 'Happy',
            'study': 'Calm',
            'summer': 'Happy',
            'work-out': 'Excited',
        }

        for genre, mood in genre_mood_mapping.items():
            train_data.loc[train_data['track_genre'].str.contains(genre, case=False), 'mood'] = mood
    
    return train_data

train_data_result = (calculate_mood_score(train_data))
test_data_result = (calculate_mood_score(test_data))

train_data.to_csv('/Users/hemmanuel/Downloads/training_data_with_mood.csv', index=False)
test_data.to_csv('/Users/hemmanuel/Downloads/data_2_with_mood_.csv', index=False)

print("Training Data: \n")
print(train_data_result)

print("Testing Data: \n")
print(test_data_result)
