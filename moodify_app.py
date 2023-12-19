from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
import secrets
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.template_folder = 'templates'

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SPOTIPY_CLIENT_ID'] = 'b6c8751ea57e47eb85f0eb7bc1603c4c'
app.config['SPOTIPY_CLIENT_SECRET'] = '3adb2ef100294261a7009958064665dc'
app.config['SPOTIPY_REDIRECT_URI'] = 'http://localhost:5001/callback'

client_credentials_manager = SpotifyClientCredentials(
    client_id='b6c8751ea57e47eb85f0eb7bc1603c4c', client_secret='3adb2ef100294261a7009958064665dc')
# Set up Spotify OAuth
sp_oauth = SpotifyOAuth(app.config['SPOTIPY_CLIENT_ID'], app.config['SPOTIPY_CLIENT_SECRET'],
                       app.config['SPOTIPY_REDIRECT_URI'], scope='user-library-modify',cache_path='.spotifycache')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

auth_url = sp_oauth.get_authorize_url()

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

    selected_mood = SelectField('Select Your Mood:', choices=mood_options, validators=[DataRequired()], id='selected_mood',name='selected_mood')

    submit = SubmitField('Get Recommendations')

def get_recommendations(selected_mood):
    try:

        # Filter the dataframe based on the selected mood
        selected_df = test_df[test_df['predicted_mood'] == selected_mood]
        print(test_df['predicted_mood'].unique())  # Print unique values in the 'predicted_mood' column
        print(selected_df)

        # Randomly select a seed track from the filtered dataframe
        seed_track_id = random.choice(selected_df['track_id'].tolist())

        recommendations = sp.recommendations(seed_tracks=[seed_track_id], limit=10)

        # Extract relevant information from the recommendations
        recommended_tracks = [
            (
                track['name'],
                ', '.join(artist['name'] for artist in track['artists']),
                track['external_urls']['spotify'],
                track['uri'],
                track.get('explicit', False)  # Include explicit information, default to False if not available
            )
            for track in recommendations['tracks']
        ]

        # Shuffle the list of recommended tracks
        random.shuffle(recommended_tracks)

        return recommended_tracks
    except Exception as e:
        return [('Error', 'An error occurred', '', '')]

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MoodForm()

    if form.validate_on_submit():
        selected_mood = form.selected_mood.data
        print("Selected Mood:", selected_mood)  # Add this line for debugging
        session['selected_mood'] = selected_mood # Store the selected mood in the session
        recommended_tracks = get_recommendations(selected_mood)
        return render_template('index.html', form=form, recommended_tracks=recommended_tracks)

    return render_template('index.html', form=form, recommended_tracks=None)


@app.route('/download', methods=['GET','POST'])
def download():
    try:
        # Get the selected track URIs from the form
        selected_tracks_uris = [uri for uri in request.form['selected_tracks_uris'].split(',') if uri]

        print("Selected Track URIs:", selected_tracks_uris)  # Print selected track URIs for debugging

        # Check if the user is already authorized
        token_info = sp_oauth.get_cached_token()

        if not token_info:
            # If not authorized, redirect the user to the Spotify login page
            return redirect(url_for('spotify_login'))
        
        # Refresh the access token if it's expired
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

        # Use the Spotify API with the obtained access token
        sp2 = spotipy.Spotify(auth=token_info['access_token'])

        # Create a new playlist with a timestamp and selected mood in the description
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        selected_mood = session.get('selected_mood')
        selected_mood = selected_mood.lower()
        playlist_name = f"moodify playlist ({selected_mood} - {timestamp})"
        playlist_description = f"created at {timestamp} based on the mood: {selected_mood}. recommended tracks by moodify."

        playlist = sp2.user_playlist_create(sp2.me()['id'], playlist_name, public=True, collaborative=False, description=playlist_description)
        sp2.playlist_add_items(playlist['id'], selected_tracks_uris)

        print("Playlist created and tracks added successfully!")

        # Redirect to the 'download_success' page or any other page you want
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error creating or adding tracks to the playlist: {e}")
        return jsonify({"error": str(e)})

@app.route('/spotify_login')
def spotify_login():
    auth_url = sp_oauth.get_authorize_url(scope='user-library-modify playlist-modify-public')
    print(f"Authorization URL: {auth_url}")
    return redirect(auth_url)

# Route for handling Spotify callback
@app.route('/callback')
def spotify_callback():
    try:
        token_info = sp_oauth.get_access_token(request.args['code'], check_cache = False)
        access_token = token_info['access_token']
        session['token_info'] = {'access_token': access_token}
        print("Token retrieved successfully!")
    except Exception as e:
        print(f"Error in callback: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.jinja_env.globals['bootstrap'] = bootstrap
    app.run(debug=True, port=5001, host='0.0.0.0')
