import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '../Population_E_All_Data_NOFLAG.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Defining developed and developing regions based on the available data classifications
developed_regions = ['European Union (27)', 'Northern America']
developing_regions = ['Africa', 'Asia', 'Central America']

# Filter data for these regions
developed_data = data[data['Area'].isin(developed_regions) & (data['Element'] == 'Total Population - Both sexes')]
developing_data = data[data['Area'].isin(developing_regions) & (data['Element'] == 'Total Population - Both sexes')]

# Selecting representative years for analysis: 1950, 1970, 1990, 2010, 2020
years = ['Y1950', 'Y1970', 'Y1990', 'Y2010', 'Y2020']

# Summing up the population for these years across the selected regions
developed_populations = developed_data[years].sum() / 1000  # converting from thousands to millions
developing_populations = developing_data[years].sum() / 1000  # converting from thousands to millions

# Creating a DataFrame for plotting
populations = pd.DataFrame({
    'Year': [int(year.strip('Y')) for year in years],
    'Developed': developed_populations.values,
    'Developing': developing_populations.values
})

# Plotting the population trends for developed vs. developing regions
plt.figure(figsize=(12, 6))
plt.plot(populations['Year'], populations['Developed'], marker='o', linestyle='-', color='blue', label='Developed')
plt.plot(populations['Year'], populations['Developing'], marker='o', linestyle='-', color='red', label='Developing')
plt.title('Population Growth Trends: Developed vs. Developing Regions (1950-2020)')
plt.xlabel('Year')
plt.ylabel('Total Population (Millions)')
plt.grid(True)
plt.legend()
plt.show()