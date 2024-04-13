import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the dataset
file_path = './Population_E_All_Data_NOFLAG.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Define the countries of interest
countries_of_interest = ['China', 'India', 'United States of America', 'Indonesia', 'Pakistan']

# Filter data for these countries and for urban population elements
filtered_data = data[(data['Area'].isin(countries_of_interest)) & (data['Element'] == 'Urban population')]

# Pivot the data to have years as columns and countries as rows
urban_data = filtered_data.pivot_table(index='Area', columns='Element Code', values=[col for col in data.columns if col.startswith('Y')])

# Correct handling of multi-index columns
urban_data.columns = [f'{col[1]}_{col[0]}' if isinstance(col, tuple) else col for col in urban_data.columns]

# Extract year columns from the multi-index columns
years = sorted(set([col.split('_')[1] for col in urban_data.columns]))

# Reset index to manipulate the data easier
urban_data.reset_index(inplace=True)

# Drop the 'Element' column and set 'Area' as index again
urban_data.set_index('Area', inplace=True)

# Drop any unnecessary columns if existent
urban_data.drop(columns='Element', inplace=True, errors='ignore')

# Prepare the dataset for regression
x = np.array([int(year[1:]) for year in years]).reshape(-1, 1)  # Year as integer
predictions = {}

# Fit a linear regression model for each country and predict future urban population up to 2100
for country in urban_data.index:
    y = urban_data.loc[country].astype(float).values.reshape(-1, 1)  # Urban populations
    model = LinearRegression().fit(x, y)
    
    # Predict from 2051 to 2100
    future_years = np.array(range(2051, 2101)).reshape(-1, 1)
    future_populations = model.predict(future_years)
    
    # Combine past and future predictions
    all_years = np.concatenate((x, future_years), axis=0)
    all_populations = np.concatenate((y, future_populations), axis=0)
    
    # Store in dictionary
    predictions[country] = all_populations.flatten()

# Create a DataFrame to display the predictions neatly
prediction_df = pd.DataFrame(predictions, index=all_years.flatten())
print(prediction_df)

# Visualization of the historical and predicted urban populations
plt.figure(figsize=(14, 8))

# Loop through each country in the predictions dictionary to plot the data
for country, populations in predictions.items():
    plt.plot(list(range(1950, 2101)), populations, label=country)

plt.title('Predicted Urban Populations (1950 - 2100)')
plt.xlabel('Year')
plt.ylabel('Urban Population (in billions)')
plt.legend()
plt.grid(True)
plt.show()