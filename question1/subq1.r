# Load required libraries
library(dplyr)
library(readr)
library(ggplot2)

# Load the dataset to examine its structure and content
file_path <- "../Population_E_All_Data_NOFLAG.csv"
data <- read_csv(file_path)

# Filter the data for the "Total Population - Both sexes" element globally
global_population <- filter(data, Element == "Total Population - Both sexes", Area == "World")

# Select the year columns from 1950 to the most recent year available
year_columns <- grep("^Y", names(global_population), value = TRUE)
global_population_years <- select(global_population, one_of(year_columns))
global_population_years <- t(global_population_years)
colnames(global_population_years) <- c("Total Population (Thousands)")

# Convert and clean data
global_population_years <- as.data.frame(global_population_years)
global_population_years$Year <- as.integer(gsub("Y", "", rownames(global_population_years)))
global_population_years$`Total Population (Millions)` <- global_population_years$`Total Population (Thousands)` / 1000

# Plotting the global population data
ggplot(data = global_population_years, aes(x = Year, y = `Total Population (Millions)`)) +
  geom_line(color = "blue", size = 1) +
  geom_point(color = "blue", size = 2) +
  labs(title = "Global Total Population (Both Sexes) from 1950 to 2024",
       x = "Year",
       y = "Total Population (Millions)") +
  theme_minimal() +
  scale_x_continuous(breaks = seq(1950, 2024, by = 5)) +
  xlim(1950, 2024) +
  theme(panel.grid.major = element_line(color = "gray", size = 0.5),
        panel.grid.minor = element_blank(),
        plot.title = element_text(hjust = 0.5))