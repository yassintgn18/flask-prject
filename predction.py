import pandas as pd

train_data = pd.read_csv("hhh.csv")

test_data = [
    {"id2": 9, "temperature2": 22, "cloud_cover2": 5, "precipitation2": 0, "wind_speed2": 2}
]

# Convert the list of dictionaries to a DataFrame
test_data_df = pd.DataFrame(test_data)

from sklearn.ensemble import RandomForestClassifier

y = train_data["statue2"]
features = ["temperature2", "cloud_cover2", "precipitation2", "wind_speed2"]
X = pd.get_dummies(train_data[features])
X_test = pd.get_dummies(test_data_df[features])
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X, y)
predictions = model.predict(X_test)
output = pd.DataFrame({'id2': test_data_df.id2, 'Statue': predictions})
# Predict probabilities for each class
probabilities = model.predict_proba(X_test)

# Convert probabilities to DataFrame
probabilities_df = pd.DataFrame(probabilities, columns=model.classes_)

# Concatenate the id2 and probabilities DataFrames
output_with_probabilities = pd.concat([test_data_df[['id2']], probabilities_df], axis=1)

print(output_with_probabilities)