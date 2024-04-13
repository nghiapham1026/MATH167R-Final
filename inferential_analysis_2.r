library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)

# Load the dataset
file_path <- './Population_E_All_Data_NOFLAG.csv'
data <- read_csv(file_path)

# Define the countries of interest
countries_of_interest <- c('China', 'India', 'United States of America', 'Indonesia', 'Pakistan')

# Filter data for these countries and for urban population elements
filtered_data <- data %>%
  filter(Area %in% countries_of_interest, Element == 'Urban population')

# Pivot the data to have years as columns and countries as rows
urban_data <- filtered_data %>%
  pivot_longer(cols = starts_with('Y'), names_to = 'Year', values_to = 'Population') %>%
  mutate(Year = as.numeric(sub('Y', '', Year))) # convert year to numeric

# Prepare the dataset for regression
predictions <- list()

# Fit a linear model for each country and predict future urban population up to 2100
urban_data %>%
  group_by(Area) %>%
  do({
    model <- lm(Population ~ Year, data = .)
    future_years <- data.frame(Year = 2051:2100)
    future_populations <- predict(model, newdata = future_years)
    predictions[[unique(.$Area)]] <- c(.$Population, future_populations) # Store predictions
    future_years$Population <- future_populations
    return(future_years)
  }) %>%
  ungroup() %>%
  pivot_wider(names_from = Area, values_from = Population)

# Display the data for the last few years to see the prediction output
print(tail(predictions, n = 5))

# Optionally, plot the predictions
plot_data <- bind_rows(lapply(names(predictions), function(country) {
  data.frame(Year = 1950:2100, Population = predictions[[country]], Country = country)
}))

ggplot(plot_data, aes(x = Year, y = Population, color = Country)) +
  geom_line() +
  labs(title = "Projected Urban Populations", x = "Year", y = "Urban Population") +
  theme_minimal()
