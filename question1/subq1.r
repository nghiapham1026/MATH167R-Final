# Load required libraries
library(dplyr)
library(readr)
library(ggplot2)
library(tidyr)

# Load the dataset to examine its structure and content
file_path <- "../Population_E_All_Data_NOFLAG.csv"
data <- read_csv(file_path)

# Define regions of interest
regions <- c("Northern America", "Africa", "Europe", "Asia", "Southern America")

# Filter the data for male and female populations by region
population_data <- filter(data, Element %in% c("Total Population - Male", "Total Population - Female"), 
                          Area %in% regions)

# Select the year columns from 1950 to the most recent year available
year_columns <- grep("^Y", names(population_data), value = TRUE)
population_data <- population_data %>%
  select(Area, Element, one_of(year_columns)) %>%
  pivot_longer(cols = starts_with("Y"), names_to = "Year", values_to = "Population") %>%
  mutate(Year = as.integer(sub("Y", "", Year)),
         Sex = ifelse(Element == "Total Population - Male", "Male", "Female"),
         Population = Population / 1000)  # Convert to millions

# Plotting the global population data by region and sex
ggplot(data = population_data, aes(x = Year, y = Population, color = Sex, linetype = Area)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(title = "Global Population by Sex and Region from 1950 to 2024",
       x = "Year",
       y = "Population (Millions)") +
  theme_minimal() +
  scale_x_continuous(breaks = seq(1950, 2024, by = 5)) +
  xlim(1950, 2024) +
  scale_color_manual(values = c("Male" = "blue", "Female" = "red")) +
  theme(panel.grid.major = element_line(color = "gray", size = 0.5),
        panel.grid.minor = element_blank(),
        plot.title = element_text(hjust = 0.5),
        legend.position = "bottom")
