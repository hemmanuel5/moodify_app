from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import secrets

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.template_folder = 'templates'

app.config['SECRET_KEY'] = secrets.token_hex(16)

# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual credentials
client_credentials_manager = SpotifyClientCredentials(client_id='b6c8751ea57e47eb85f0eb7bc1603c4c', client_secret='3adb2ef100294261a7009958064665dc')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

test_df = pd.read_csv('/Users/hemmanuel/Downloads/data_2_with_predicted_mood.csv')

class MoodForm(FlaskForm):
    mood_options = [
        ("Excited", "excited"),
        ("Happy", "happy"),
        ("Calm", "calm"),
        ("Tired", "tired"),
        ("Bored", "bored"),
        ("Sad", "sad"),
        ("Nervous", "nervous"),
        ("Angry", "angry"),
        ("Stressed", "stressed")
    ]

    selected_mood = SelectField('Select Your Mood:', choices=mood_options, validators=[DataRequired()])

def get_recommendations(selected_mood):
    try:
        # Filter the dataframe based on the selected mood
        selected_df = test_df[test_df['predicted_mood'] == selected_mood]

        # Randomly select a seed track from the filtered dataframe
        seed_track_id = random.choice(selected_df['track_id'].tolist())

        recommendations = sp.recommendations(seed_tracks=[seed_track_id], limit=10)

        # Extract relevant information from the recommendations
        recommended_tracks = [
            (track['name'], ', '.join(artist['name'] for artist in track['artists']), track['external_urls']['spotify'])
            for track in recommendations['tracks']
        ]

        # Shuffle the list of recommended tracks
        random.shuffle(recommended_tracks)

        return recommended_tracks
    except Exception as e:
        return [('Error', 'An error occurred', '')]

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MoodForm()

    if form.validate_on_submit():
        selected_mood = form.selected_mood.data
        recommended_tracks = get_recommendations(selected_mood)
        return render_template('index.html', form=form, recommended_tracks=recommended_tracks)

    return render_template('index.html', form=form, recommended_tracks=None)

if __name__ == '__main__':
    app.jinja_env.globals['bootstrap'] = bootstrap
    app.run(debug=True, port=5001, host='0.0.0.0')

