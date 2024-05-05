library(readr)
library(dplyr)
library(ggplot2)

# Load the dataset
file_path <- "../Population_E_All_Data_NOFLAG.csv"
data <- read_csv(file_path)

# Defining developed and developing regions based on the available data classifications
developed_regions <- c('European Union (27)', 'Northern America')
developing_regions <- c('Africa', 'Asia', 'Central America')

# Filter data for these regions
developed_data <- filter(data, Area %in% developed_regions, Element == "Total Population - Both sexes")
developing_data <- filter(data, Area %in% developing_regions, Element == "Total Population - Both sexes")

# Selecting representative years for analysis: 1950, 1970, 1990, 2010, 2020
years <- c('Y1950', 'Y1970', 'Y1990', 'Y2010', 'Y2020')

# Summing up the population for these years across the selected regions
developed_populations <- colSums(select(developed_data, all_of(years))) / 1000  # converting from thousands to millions
developing_populations <- colSums(select(developing_data, all_of(years))) / 1000  # converting from thousands to millions

# Creating a data frame for plotting
populations <- data.frame(
  Year = as.numeric(sub("Y", "", years)),
  Developed = as.numeric(developed_populations),
  Developing = as.numeric(developing_populations)
)

# Plotting the population trends for developed vs. developing regions
ggplot(populations, aes(x = Year)) +
  geom_line(aes(y = Developed, color = "Developed"), size = 1, linetype = "solid") +
  geom_line(aes(y = Developing, color = "Developing"), size = 1, linetype = "solid") +
  geom_point(aes(y = Developed, color = "Developed"), size = 2) +
  geom_point(aes(y = Developing, color = "Developing"), size = 2) +
  scale_color_manual(values = c("Developed" = "blue", "Developing" = "red")) +
  labs(title = "Population Growth Trends: Developed vs. Developing Regions (1950-2020)",
       x = "Year",
       y = "Total Population (Millions)",
       color = "Region") +
  theme_minimal() +
  theme(legend.position = "bottom")