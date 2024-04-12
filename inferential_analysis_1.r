library(dplyr)
library(readr)

population_data <- read_csv("./Population_E_All_Data_NOFLAG.csv")

# Filter for total population data (both sexes)
total_population_data <- population_data %>%
  filter(Element == "Total Population - Both sexes", Unit == "1000 No")

# Calculate growth rate from 1950 to 2023
total_population_data <- total_population_data %>%
  mutate(`Growth Rate (%)` = ((Y2023 - Y1950) / Y1950) * 100)

# Sort the data by growth rate to find the top countries with the fastest growth
fastest_growing_countries <- total_population_data %>%
  select(Area, Y1950, Y2023, `Growth Rate (%)`) %>%
  arrange(desc(`Growth Rate (%)`))

# Print the top 5 countries with the highest growth rates
print(head(fastest_growing_countries, 5))