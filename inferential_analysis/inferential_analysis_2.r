library(readr)
library(dplyr)
library(tidyr)
library(purrr)  # Ensure this is added
library(ggplot2)

# Load the dataset
file_path <- '../Population_E_All_Data_NOFLAG.csv'
data <- read_csv(file_path)

# Define the countries of interest
countries_of_interest <- c('China', 'India', 'United States of America', 'Indonesia', 'Pakistan')

# Filter data for these countries and for urban population elements
filtered_data <- data %>%
  filter(Area %in% countries_of_interest, Element == 'Urban population')

# Pivot the data to have years as columns and countries as rows
urban_data <- filtered_data %>%
  pivot_longer(cols = starts_with('Y'), names_to = 'Year', values_to = 'Population') %>%
  mutate(Year = as.numeric(sub('Y', '', Year)))  # Convert year to numeric

# Prepare data for regression
urban_data <- urban_data %>%
  group_by(Area) %>%
  nest()

# Define a function to predict populations
predict_population <- function(df) {
  model <- lm(Population ~ Year, data = df)
  future_years <- data.frame(Year = 2051:2100)
  future_populations <- predict(model, newdata = future_years)
  data.frame(Year = c(df$Year, future_years$Year),
             Population = c(df$Population, future_populations))
}

# Apply the function to each group and gather predictions
predictions <- urban_data %>%
  mutate(Predictions = map(data, ~ predict_population(.))) %>%
  unnest(c(Predictions))

print(tail(predictions))