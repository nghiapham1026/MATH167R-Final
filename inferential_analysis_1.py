import pandas as pd
from scipy import stats

# Load the dataset to examine its first few rows and structure
file_path = './Population_E_All_Data_NOFLAG.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Identify the earliest and latest years available in the data
years = [col for col in data.columns if col.startswith('Y')]
earliest_year, latest_year = years[0], years[-1]

# Filter data for global urban and rural population statistics
urban_rural_data = data[data['Element'].isin(['Rural population', 'Urban population'])]

# Filter data for the specific continents and for urban and rural population elements
continents = ['Europe', 'Asia', 'Africa', 'Northern America', 'South America']
continent_data = urban_rural_data[urban_rural_data['Area'].isin(continents)]

# Correctly group and unstack the data to prepare it for analysis
continent_summary = continent_data.groupby(['Area', 'Element']).sum().unstack(level=-1)

# Extract population data for both urban and rural for the years 1950 and 2015
population_1950 = continent_summary.loc[:, ('Y1950', slice(None))]
population_2015 = continent_summary.loc[:, ('Y2015', slice(None))]

# Calculate total population for both years
total_population_1950 = population_1950.sum(axis=1)
total_population_2015 = population_2015.sum(axis=1)

# Calculate urban and rural percentages for 1950 and 2015
urban_percent_1950 = (population_1950['Y1950', 'Urban population'] / total_population_1950) * 100
rural_percent_1950 = (population_1950['Y1950', 'Rural population'] / total_population_1950) * 100
urban_percent_2015 = (population_2015['Y2015', 'Urban population'] / total_population_2015) * 100
rural_percent_2015 = (population_2015['Y2015', 'Rural population'] / total_population_2015) * 100

# Create a DataFrame for comparative analysis
comparison_df = pd.DataFrame({
    'Continent': total_population_1950.index,
    'Urban % 1950': urban_percent_1950.values,
    'Rural % 1950': rural_percent_1950.values,
    'Urban % 2015': urban_percent_2015.values,
    'Rural % 2015': rural_percent_2015.values
})

print(comparison_df)

# Paired t-test
t_statistic, p_value = stats.ttest_rel(comparison_df['Urban % 1950'], comparison_df['Urban % 2015'])

# Display results
print('t-statistic:', t_statistic)
print('p-value:', p_value)

# Determine significance
alpha = 0.05  # Common threshold for significance
if p_value < alpha:
    print("The change in urban population percentage is statistically significant.")
else:
    print("The change in urban population percentage is not statistically significant.")