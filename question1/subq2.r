library(readr)
library(dplyr)
library(ggplot2)

# Load the dataset
file_path <- '../Population_E_All_Data_NOFLAG.csv'
data <- read_csv(file_path)

# Filter the data for the "Total Population - Both sexes" element globally
global_population <- filter(data, Element == "Total Population - Both sexes", Area == "World")

# Select the year columns from 1950 to the most recent year available
year_columns <- names(global_population)[grepl("^Y", names(global_population))]
global_population_years <- t(select(global_population, one_of(year_columns)))

# Reset the index to turn years into a column and convert the population from thousands to millions
global_population_years <- as.data.frame(global_population_years)
colnames(global_population_years) <- c("Total Population (Thousands)")
global_population_years$Year <- as.numeric(gsub("Y", "", rownames(global_population_years)))
global_population_years$`Total Population (Millions)` <- as.numeric(global_population_years$`Total Population (Thousands)`) / 1000

# Filter data for "Total Population - Both sexes" element for all countries
country_population <- filter(data, Element == "Total Population - Both sexes")

# Select necessary columns
country_population_growth <- select(country_population, Area, Y1950, Y2024)

# Convert population data from thousands to millions and calculate annual growth rate
country_population_growth <- mutate(country_population_growth,
                                     Y1950 = Y1950 / 1000,
                                     Y2024 = Y2024 / 1000,
                                     Annual_Growth_Rate = ((Y2024 / Y1950) ^ (1 / (2024 - 1950)) - 1) * 100)

# Sort by annual growth rate in descending order and pick the top countries
country_population_growth_sorted <- arrange(country_population_growth, desc(Annual_Growth_Rate))
top_countries <- head(country_population_growth_sorted, 20)

# Plotting the annualized growth rates
ggplot(top_countries, aes(x = reorder(Area, Annual_Growth_Rate), y = Annual_Growth_Rate, fill = Area)) +
  geom_bar(stat = "identity") +
  labs(x = "Country", y = "Annual Growth Rate (%)", title = "Top 20 Countries by Growth Rate from 1950 to 2024") +
  coord_flip() +  # This makes it a horizontal bar chart
  theme_minimal()