from sklearn import datasets
import numpy as np
import pandas as pd

# Load the iris dataset
iris = datasets.load_iris()

# Convert the data into a DataFrame
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Print the first few rows of the DataFrame
print(df.head())

# Convert categorical variables to numerical values
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['species'] = le.fit_transform(df['species'])

# Drop the 'species' column
df = df.drop('species', axis=1)

# Print the first few rows of the DataFrame after dropping the species column
print(df.head())