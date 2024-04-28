# Load necessary libraries
library(dplyr)
library(readr)
library(tidyverse)

# Load the dataset
file_path <- '../Population_E_All_Data_NOFLAG.csv'
data <- read_csv(file_path, locale = locale(encoding = "Latin1"))

# Extract relevant columns
relevant_years <- c("Y1950", "Y2015") # Filter to only these years for urban and rural
data <- data %>%
  filter(Element %in% c('Rural population', 'Urban population')) %>%
  select(Area, Element, all_of(relevant_years))

# Aggregate data to calculate sums for each area and element
data_summary <- data %>%
  group_by(Area, Element) %>%
  summarise(across(everything(), sum, na.rm = TRUE)) %>%
  pivot_wider(names_from = Element, values_from = c("Y1950", "Y2015"))

# Calculate total populations and urbanization percentages
data_summary <- data_summary %>%
  mutate(Total_1950 = `Y1950_Rural population` + `Y1950_Urban population`,
         Total_2015 = `Y2015_Rural population` + `Y2015_Urban population`,
         Urban_Percent_1950 = `Y1950_Urban population` / Total_1950 * 100,
         Urban_Percent_2015 = `Y2015_Urban population` / Total_2015 * 100)

# Perform paired t-test
t_test_result <- t.test(data_summary$Urban_Percent_1950, data_summary$Urban_Percent_2015, paired = TRUE)

# Output results
print(t_test_result)

# Check for statistical significance
alpha <- 0.05
if (t_test_result$p.value < alpha) {
  print("The change in urban population percentage is statistically significant.")
} else {
  print("The change in urban population percentage is not statistically significant.")
}