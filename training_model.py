import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load and drop columns from the training data only if they haven't been dropped
train_data = pd.read_csv('/Users/hemmanuel/Downloads/training_data_with_mood.csv')
columns_to_drop = ['dataset (1)', 'album_name', 'time_signature', 'track_genre']

if any(col in train_data.columns for col in columns_to_drop):
    train_data = train_data.drop(columns_to_drop, axis=1)
    train_data.to_csv('/Users/hemmanuel/Downloads/training_data_with_mood.csv', index=False)

# Load and drop columns from the testing data only if they haven't been dropped
test_data = pd.read_csv('/Users/hemmanuel/Downloads/data_2_with_mood_.csv')
test_data.rename(columns={'id': 'track_id', 'name': 'track_name'}, inplace=True)
columns_to_drop_test = ['release_date', 'year']

if any(col in test_data.columns for col in columns_to_drop_test):
    test_data = test_data.drop(columns_to_drop_test, axis=1)
    test_data.to_csv('/Users/hemmanuel/Downloads/data_2_with_mood_', index=False)

# Assuming 'mood' is your target variable and other columns are features
X_train = train_data[['valence','acousticness','danceability',
                    'duration_ms','energy','explicit','instrumentalness',
                    'key','liveness','loudness','mode',
                    'popularity','speechiness','tempo']]

y_train = train_data['mood']

# Assuming the testing set has similar columns as the training set
X_test = test_data[['valence','acousticness','danceability',
                    'duration_ms','energy','explicit','instrumentalness',
                    'key','liveness','loudness','mode',
                    'popularity','speechiness','tempo']]
y_test = test_data['mood']

# Initialize the Decision Tree model
model = DecisionTreeClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Add the predicted mood to the testing data
test_data['predicted_mood'] = predictions

# Print or save the testing data with predicted mood
print(test_data[['track_id', 'track_name', 'predicted_mood']])

# Save the testing data with predicted mood to a new CSV file
test_data.to_csv('/Users/hemmanuel/Downloads/data_2_with_predicted_mood.csv', index=False)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

print(train_data['mood'].unique())

