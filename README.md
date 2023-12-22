# moodify

<p align="center">
  <img width="351" alt="Screen Shot 2023-12-21 at 9:43:24 PM" src="https://raw.githubusercontent.com/hemmanuel5/moodify_app/main/assets/126534510/2ea943ad-3a88-4abc-b6d0-8eb3afabd560">
</p>

The moodify app is a Python-based application that analyzes music data to determine the mood of a track and provides personalized recommendations based on the user's mood. The application consists of three main scripts: `calculate_mood_score.py`, `training_model.py`, and `moodify_app.py`. This README provides information on each script and instructions for setting up and running the moodify app.

## Table of Contents
- [Scripts](#scripts)
  - [calculate_mood_score.py](#calculate_mood_scorepy)
  - [training_model.py](#training_modelpy)
  - [moodify_app.py](#moodify_apppy)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Known Issues and Bugs](#known-issues-and-bugs)
- [References](#references)

## Scripts

### `calculate_mood_score.py`

This script calculates a mood score based on audio features and assigns specific moods to each track. It also considers genre information and updates the mood labels accordingly.

### `training_model.py`

This script loads training and testing data, preprocesses it, trains a Decision Tree model, and evaluates the model's accuracy. It also adds the predicted mood to the testing data and saves the data with the predicted mood to a new CSV file.

### `moodify_app.py`

This script implements a Flask web application that allows users to input their mood and receive personalized music recommendations. It interacts with the Spotify API to create and download playlists.


## Getting Started

### Prerequisites

- Python 3.11
- Flask
- Spotipy
- Pandas
- Scikit-learn
- Bootstrap

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/moodify_app.git
   cd moodify_app
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the `calculate_mood_score.py` script to calculate mood scores and assign moods to tracks.

   ```bash
   python calculate_mood_score.py
   ```

2. Run the `training_model.py` script to train the Decision Tree model and generate predictions.

   ```bash
   python training_model.py
   ```

3. Run the `moodify_app.py` script to start the Flask web application.

   ```bash
   python moodify_app.py
   ```

4. Open a web browser and go to [http://localhost:5001](http://localhost:5001) to access the moodify app.


## Known Issues and Bugs

# 1. Authorization Redirect Issue

**Description:**
Clicking the "Download" button is expected to redirect users to the Spotify login page for account authorization. However, there may be instances where the redirection does not occur as expected.

**Workaround:**
If you encounter this issue, please ensure you are not already logged in to Spotify. If the problem persists, try refreshing the page or opening the app in an incognito/private browsing window.

# 2. Playlist Description Display Issue

**Description:**
The playlist description may not always appear when downloading a playlist.

**Workaround:**
If the playlist description is missing, you can manually add the description when importing the playlist into your Spotify account.

# 3. Deployment Troubles and Requirements.txt

**Description:** 
There are difficulties deploying the application, and there might be issues with the `requirements.txt` file.

**Workaround:**
  - Double-check the contents of `requirements.txt` to ensure all necessary dependencies and versions are specified correctly.
  - Verify that your deployment environment is compatible with the specified dependencies.
  - Check for error messages during deployment

# 4. Favicon Not Showing Up

**Description:** The favicon specified in the `index.html` file may not be displayed.

**Workaround:** Verify the path and file format of the favicon. Ensure it is correctly referenced in the HTML file, and the file is accessible.


## References

The development of the moodify app was influenced and guided by discussions and assistance from the following sources:

- ChatGPT and the OpenAI community
- Reddit communities: r/python, r/flask
- [Training Data](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset)
- [Testing Data](https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset/input)
- [Spotipy Documentation](https://spotipy.readthedocs.io/en/2.22.1/#api-reference)
- [Spotify Developer Documentation](https://developer.spotify.com/documentation/web-api)
- [Medium Article](https://towardsdatascience.com/build-your-first-mood-based-music-recommendation-system-in-python-26a427308d96)
- [Music Mood Prediction Based on Spotify’s AudioFeatures Using Logistic Regression research paper](https://www.researchgate.net/publication/370450676_Music_Mood_Prediction_Based_on_Spotify's_Audio_Features_Using_Logistic_Regression)
  

