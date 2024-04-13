import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the dataset to examine its first few rows and structure
file_path = './Population_E_All_Data_NOFLAG.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Define the countries of interest
countries_of_interest = ['China', 'India', 'United States of America', 'Indonesia', 'Pakistan']

# Filter data for these countries and for urban and rural population elements
filtered_data = data[(data['Area'].isin(countries_of_interest)) & (data['Element'].isin(['Urban population', 'Rural population']))]

# Pivot the data to have years as columns and countries, elements as rows
urban_rural_data = filtered_data.pivot_table(index=['Area', 'Element'], columns='Element Code', values=[col for col in data.columns if col.startswith('Y')])

# Correct handling of multi-index columns
urban_rural_data.columns = [f'{col[1]}_{col[0]}' if isinstance(col, tuple) else col for col in urban_rural_data.columns]

# Separate urban and rural data for easier manipulation
urban_data = urban_rural_data[[col for col in urban_rural_data.columns if '561' in col]]
rural_data = urban_rural_data[[col for col in urban_rural_data.columns if '551' in col]]

# Extract year columns from the multi-index columns
years = sorted(set([col.split('_')[1] for col in urban_data.columns]))

# Calculate urbanization rates
urbanization_rates = pd.DataFrame(index=urban_data.index)

for year in years:
    urban_population = urban_data[f'561_{year}']
    rural_population = rural_data[f'551_{year}']
    total_population = urban_population + rural_population
    urbanization_rates[year] = (urban_population / total_population) * 100

# Reset index to manipulate the data easier
urban_data.reset_index(inplace=True)
rural_data.reset_index(inplace=True)

# Filter urban and rural data again to ensure correct handling
urban_data = urban_data[urban_data['Element'] == 'Urban population']
rural_data = rural_data[rural_data['Element'] == 'Rural population']

# Remove 'Element' column and set 'Area' as index again
urban_data.set_index('Area', inplace=True)
rural_data.set_index('Area', inplace=True)

# Drop the 'Element' column now from both dataframes
urban_data.drop(columns='Element', inplace=True, errors='ignore')
rural_data.drop(columns='Element', inplace=True, errors='ignore')

# Calculate urbanization rates
urbanization_rates_final = pd.DataFrame(index=urban_data.index)
for year in years:
    urban_population = urban_data[f'561_{year}'].astype(float)
    rural_population = rural_data[f'551_{year}'].astype(float)
    total_population = urban_population + rural_population
    urbanization_rates_final[year] = (urban_population / total_population) * 100

print(urbanization_rates_final.head())

# Prepare the dataset for regression
x = np.array([int(year[1:]) for year in urbanization_rates_final.columns]).reshape(-1, 1)  # Year as integer
predictions = {}

# Fit a linear regression model for each country and predict urbanization rates up to 2100
for country in urbanization_rates_final.index:
    y = urbanization_rates_final.loc[country].values.reshape(-1, 1)  # Urbanization rates
    model = LinearRegression().fit(x, y)
    
    # Predict from 2051 to 2100
    future_years = np.array(range(2051, 2101)).reshape(-1, 1)
    future_rates = model.predict(future_years)
    
    # Combine past and future predictions
    all_years = np.concatenate((x, future_years), axis=0)
    all_rates = np.concatenate((y, future_rates), axis=0)
    
    # Store in dictionary
    predictions[country] = all_rates.flatten()

# Create a DataFrame to display the predictions neatly
prediction_df = pd.DataFrame(predictions, index=all_years.flatten())
print(prediction_df.tail())