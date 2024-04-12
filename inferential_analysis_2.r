# Load necessary libraries
library(dplyr)
library(readr)
library(tidyr)

# Load the dataset
population_data <- read_csv("./Population_E_All_Data_NOFLAG.csv")

# Filter for global total population data (both sexes)
global_population_data <- population_data %>%
  filter(grepl("World", Area, ignore.case = TRUE) & Element == "Total Population - Both sexes" & Unit == "1000 No")

# Sum up the population for each year from 1950 to 2023
global_annual_population <- global_population_data %>%
  select(starts_with("Y")) %>%
  summarise_all(sum) %>%
  mutate(across(everything(), ~ .x * 1000)) # Convert from '1000s' to absolute numbers

# Convert to a long format for easier manipulation
global_annual_population_long <- pivot_longer(global_annual_population,
                                              cols = everything(),
                                              names_to = "Year",
                                              values_to = "Population")

# Calculate year-on-year changes
global_annual_population_long <- global_annual_population_long %>%
  arrange(Year) %>%
  mutate(Yearly_Change = Population - lag(Population))

# Print the results
print(global_annual_population_long)