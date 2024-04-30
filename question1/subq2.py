import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '../Population_E_All_Data_NOFLAG.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Filter the data for the "Total Population - Both sexes" element globally
global_population = data[(data['Element'] == 'Total Population - Both sexes') & (data['Area'] == 'World')]

# Select the year columns from 1950 to the most recent year available
year_columns = global_population.columns[global_population.columns.str.startswith('Y')]
global_population_years = global_population[year_columns].transpose()

# Reset the index to turn years into a column and convert the population from thousands to millions
global_population_years.reset_index(inplace=True)
global_population_years.columns = ['Year', 'Total Population (Millions)']
global_population_years['Year'] = global_population_years['Year'].str.replace('Y', '').astype(int)
global_population_years['Total Population (Millions)'] /= 1000

# Filter data for "Total Population - Both sexes" element for all countries
country_population = data[(data['Element'] == 'Total Population - Both sexes')]

# Select necessary columns
country_population_growth = country_population[['Area', 'Y1950', 'Y2024']]

# Convert population data from thousands to millions and calculate annual growth rate
country_population_growth['Y1950'] = country_population_growth['Y1950'] / 1000
country_population_growth['Y2024'] = country_population_growth['Y2024'] / 1000
number_of_years = 2024 - 1950
country_population_growth['Annual Growth Rate (%)'] = (
    (country_population_growth['Y2024'] / country_population_growth['Y1950']) ** (1 / number_of_years) - 1) * 100

# Sort by annual growth rate in descending order and pick the top countries
country_population_growth_sorted = country_population_growth.sort_values(
    by='Annual Growth Rate (%)', ascending=False).head(20)

# Plotting the annualized growth rates
plt.figure(figsize=(14, 8))
plt.barh(country_population_growth_sorted['Area'], country_population_growth_sorted['Annual Growth Rate (%)'], color='green')
plt.xlabel('Annual Growth Rate (%)')
plt.title('Top 10 Countries by Annualized Population Growth Rate from 1950 to 2024')
plt.gca().invert_yaxis()  # Invert y-axis to have the country with highest growth at top
plt.show()