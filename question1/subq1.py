import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset to examine its structure and content
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
global_population_years['Total Population (Millions)'] /= 1000  # converting from thousands to millions

# Plotting the global population data
plt.figure(figsize=(12, 6))
plt.plot(global_population_years['Year'], global_population_years['Total Population (Millions)'], marker='o', linestyle='-', color='b')
plt.title('Global Total Population (Both Sexes) from 1950 to 2024')
plt.xlabel('Year')
plt.ylabel('Total Population (Billions)')
plt.grid(True)
plt.xticks(range(1950, 2025, 5))  # Adjust the x-axis to show every 5 years for clarity
plt.xlim(1950, 2024)  # Set the x-axis limits to focus on 1950 to 2024
plt.tight_layout()  # Adjusts plot parameters to give some padding

plt.show()