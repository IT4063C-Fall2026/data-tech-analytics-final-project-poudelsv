#!/usr/bin/env python
# coding: utf-8

# # Economic Development, Life Expectancy, and CO₂ Emissions📝
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# - I would like to analyze how the per capita GDP, the life expectancy,
# and the CO₂ emission per person have changed in Nepal, India, the United
# States, the United Kingdom, and China between 2010 and 2023. The two
# countries that I want to look into are Nepal and India due to my personal
# connection with them.
# 
# The problem lies in how the economic and health development can affect the environment. These five countries represent quite different economies, and analyzing
# how similar measures change for all of them can be interesting. This
# research will show some patterns and relationships; no cause-and-effect
# claims will be made about the GDP and changes in other measures.

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
# - My main research question is: How have the trends in GDP per capita,
# life expectancy, and CO₂ emissions per capita developed together in
# these five countries between 2010 and 2023?
# 
# I am going to address these particular questions:
# 
# 1. What were the trends in each variable in each country?
# 2. What countries in the most recent year for which I have data have had
#    life expectancies that are high or low compared to their GDP per
#    capita?
# 3. Within each country, what years that have had high GDP per capita also
#    have had high CO₂ emissions per capita?

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# - GDP per capita and life expectancy will tend to correlate positively; however,
# there might be differences in how GDP and CO₂ emissions correlate. This is a
# hypothesis, not a conclusion.
# 
# The response will consist of three line graphs with years on the horizontal
# axis and one variable on the vertical axis. Each country will have its separate
# line. In addition, there will be a scatterplot for GDP per capita vs life
# expectancy, with GDP on the horizontal axis and life expectancy on the
# vertical axis and different colors representing different countries. Another
# scatterplot will be made for GDP per capita and CO₂ emissions per person.
# 
# Specific details revealed by the graphs will be pointed out; complete data
# for some years will be indicated, along with missing data points for some
# countries.

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 
# | Dataset | Type | Fields I will use | Source |
# | --- | --- | --- | --- |
# | GDP per capita, constant 2015 US$ | World Bank JSON API | Country code, year, GDP per capita | https://data.worldbank.org/indicator/NY.GDP.PCAP.KD |
# | Life expectancy | Our World in Data CSV file | Code, Year, life expectancy | https://ourworldindata.org/grapher/life-expectancy |
# | CO₂ emissions per capita | Our World in Data CSV file | Code, Year, tonnes per person | https://ourworldindata.org/grapher/co-emissions-per-capita |
# 
# These are three distinct datasets and two data types: JSON from an API and
# CSV files. I will join them on three-letter country code and calendar year.
# For example, Nepal's 2020 GDP record will match Nepal's 2020 life expectancy
# and CO₂ records. I will check for missing values and retain the country-years
# where all three measures are available.

# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 
# - I'll get the GDP per capita from the World Bank API, and I'll import
# life expectancy and per capita carbon dioxide emissions from two CSV
# datasets. I'll filter the data by Nepal, India, the United States,
# the United Kingdom, and China for the period 2010–2023. And then I'll
# merge the datasets by the country codes and years and check for missing
# values among the merged rows.
# 
# Here is the code that demonstrates the joining of all three sources
# in one dataset. It shows that they can be joined, which will be used
# for creating the visualizations at a further stage of the work.

# In[1]:


get_ipython().run_line_magic('pip', 'install pandas requests')


# In[2]:


import pandas as pd
import requests

COUNTRIES = ["NPL", "IND", "USA", "GBR", "CHN"]
START_YEAR = 2010
END_YEAR = 2023

# Source 1: World Bank JSON API
world_bank_url = (
    "https://api.worldbank.org/v2/country/all/"
    "indicator/NY.GDP.PCAP.KD"
)

response = requests.get(
    world_bank_url,
    params={
        "format": "json",
        "date": f"{START_YEAR}:{END_YEAR}",
        "per_page": 10000,
    },
    timeout=60,
)
response.raise_for_status()
world_bank_result = response.json()

gdp_df = pd.DataFrame(
    {
        "Code": item["countryiso3code"],
        "Year": int(item["date"]),
        "gdp_per_capita": item["value"],
    }
    for item in world_bank_result[1]
    if item["countryiso3code"] in COUNTRIES
)

print("World Bank GDP rows:", len(gdp_df))
display(gdp_df.head())


# In[3]:


# Source 2: Life expectancy CSV
life_url = "https://ourworldindata.org/grapher/life-expectancy.csv"

life_raw = pd.read_csv(
    life_url,
    storage_options={"User-Agent": "Our World In Data data fetch/1.0"}
)

life_df = life_raw[["Code", "Year", life_raw.columns[3]]].copy()
life_df.columns = ["Code", "Year", "life_expectancy"]

life_df = life_df[
    life_df["Code"].isin(COUNTRIES)
    & life_df["Year"].between(START_YEAR, END_YEAR)
]

print("Life expectancy rows:", len(life_df))
display(life_df.head())


# In[4]:


# Source 3: CO2 emissions per capita CSV
co2_url = "https://ourworldindata.org/grapher/co-emissions-per-capita.csv"

co2_raw = pd.read_csv(
    co2_url,
    storage_options={"User-Agent": "Our World In Data data fetch/1.0"}
)

co2_df = co2_raw[["Code", "Year", co2_raw.columns[3]]].copy()
co2_df.columns = ["Code", "Year", "co2_tonnes_per_person"]

co2_df = co2_df[
    co2_df["Code"].isin(COUNTRIES)
    & co2_df["Year"].between(START_YEAR, END_YEAR)
]

print("CO2 rows:", len(co2_df))
display(co2_df.head())


# In[5]:


project_df = (
    gdp_df
    .merge(life_df, on=["Code", "Year"], how="inner")
    .merge(co2_df, on=["Code", "Year"], how="inner")
    .dropna()
    .sort_values(["Code", "Year"])
)

print("Complete country-year rows:", len(project_df))
print("Countries:", sorted(project_df["Code"].unique()))
print("Years:", project_df["Year"].min(), "to", project_df["Year"].max())
display(project_df.head(10))


# ## Resources and References
# *What resources and references have you used for this project?*
# - World Bank, GDP per capita (constant 2015 US$):
#   https://data.worldbank.org/indicator/NY.GDP.PCAP.KD
# - Our World in Data, Life expectancy:
#   https://ourworldindata.org/grapher/life-expectancy
# - Our World in Data, CO₂ emissions per capita:
#   https://ourworldindata.org/grapher/co-emissions-per-capita
# - World Bank Indicators API documentation:
#   https://datahelpdesk.worldbank.org/knowledgebase/articles/898581

# In[6]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')


# ## Checkpoint 2: Exploratory Data Analysis
# 
# This section explores GDP per capita, life expectancy,
# and CO₂ emissions across five countries from 2010–2023.
# 
# We will examine statistical summaries, missing values,
# duplicates, data types, and correlations.

# In[7]:


# Merge datasets before removing missing values
eda_df = (
    gdp_df.merge(life_df, on=["Code", "Year"], how="outer")
    .merge(co2_df, on=["Code", "Year"], how="outer")
)

# Statistical summary
display(eda_df.describe())

# Missing values
print("Missing values:")
print(eda_df.isnull().sum())

# Duplicate records
print("\nDuplicates:")
print(eda_df.duplicated(subset=["Code", "Year"]).sum())

# Data types
print("\nData types:")
print(eda_df.dtypes)

# Correlations
print("\nCorrelations:")
display(eda_df.select_dtypes(include="number").drop(columns="Year").corr())


# **Interpretation:**
# 
# This visualization compares the economic development of five
# countries between 2010 and 2023. GDP per capita differs
# significantly across countries, highlighting differences in
# economic development. Changes in the lines show periods
# of economic growth or decline.

# ### Visualization 2: Life Expectancy (2010–2023)
# 
# This line chart compares life expectancy across five countries
# to identify improvements, declines, and differences in health outcomes.

# In[8]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=eda_df,
    x="Year",
    y="life_expectancy",
    hue="Code",
    marker="o"
)

plt.title("Life Expectancy by Country (2010–2023)")
plt.xlabel("Year")
plt.ylabel("Life Expectancy (Years)")
plt.legend(title="Country")
plt.grid(True)
plt.show()


# **Interpretation:**
# 
# This visualization shows how life expectancy changed between
# 2010 and 2023 across the five countries. It helps identify
# long-term improvements in population health and any periods
# of decline, including possible disruptions around 2020–2021.
# 
# Differences between countries suggest that economic development
# alone may not fully explain life expectancy outcomes.

# ### Visualization 3: CO₂ Emissions per Capita (2010–2023)
# 
# This chart compares annual CO₂ emissions per person across
# five countries to identify environmental trends.

# In[9]:


plt.figure(figsize=(12, 6))

sns.lineplot(
    data=eda_df,
    x="Year",
    y="co2_tonnes_per_person",
    hue="Code",
    marker="o"
)

plt.title("CO₂ Emissions per Capita (2010–2023)")
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions (Tonnes per Person)")
plt.legend(title="Country")
plt.grid(True)
plt.show()


# **Interpretation:**
# 
# This visualization compares CO₂ emissions per person
# across five countries between 2010 and 2023.
# 
# It helps identify differences in environmental impact,
# changes in emission trends, and whether economic
# development is associated with higher emissions.
# 
# Changes over time may reflect differences in energy
# consumption, industrialization, and environmental policies.

# ### Visualization 4: GDP per Capita vs. Life Expectancy
# 
# This scatterplot examines the relationship between economic
# development and life expectancy across five countries.

# In[10]:


plt.figure(figsize=(12, 6))

sns.scatterplot(
    data=eda_df,
    x="gdp_per_capita",
    y="life_expectancy",
    hue="Code",
    s=100
)

plt.title("GDP per Capita vs. Life Expectancy (2010–2023)")
plt.xlabel("GDP per Capita (Constant 2015 US$)")
plt.ylabel("Life Expectancy (Years)")
plt.legend(title="Country")
plt.grid(True)
plt.show()


# **Interpretation:**
# 
# This scatterplot explores whether countries with higher GDP
# per capita also tend to have higher life expectancy.
# 
# The visualization allows us to compare economic and health
# outcomes across countries and identify differences in how
# these variables relate.
# 
# Any relationship observed represents correlation rather
# than causation. Other factors, including healthcare access,
# education, and public policy, may influence life expectancy.

# ## Data Cleaning and Transformation
# 
# This section checks and handles missing values, duplicates,
# data types, and potential outliers.
# 
# Missing values will be removed if necessary. Duplicate
# country-year records will be removed, and numerical columns
# will be converted to appropriate data types.
# 
# Potential outliers will be examined rather than automatically
# removed because differences between countries are meaningful
# to this analysis.

# In[11]:


# Create a copy for cleaning
clean_df = eda_df.copy()

print("Rows before cleaning:", len(clean_df))

# Remove duplicate country-year records
clean_df = clean_df.drop_duplicates(
    subset=["Code", "Year"]
)

# Convert data types
clean_df["Year"] = pd.to_numeric(
    clean_df["Year"], errors="coerce"
)

numeric_cols = [
    "gdp_per_capita",
    "life_expectancy",
    "co2_tonnes_per_person"
]

for col in numeric_cols:
    clean_df[col] = pd.to_numeric(
        clean_df[col], errors="coerce"
    )

# Remove rows missing required measurements
clean_df = clean_df.dropna(
    subset=["Code", "Year"] + numeric_cols
)

clean_df["Year"] = clean_df["Year"].astype(int)

# Validate values
clean_df = clean_df[
    (clean_df["gdp_per_capita"] > 0) &
    (clean_df["life_expectancy"].between(0, 120)) &
    (clean_df["co2_tonnes_per_person"] >= 0)
]

clean_df = clean_df.sort_values(
    ["Code", "Year"]
).reset_index(drop=True)

print("Rows after cleaning:", len(clean_df))
print("\nMissing values:")
print(clean_df.isnull().sum())
print("\nDuplicates:",
      clean_df.duplicated(["Code", "Year"]).sum())

display(clean_df.head())


# ### Cleaning Results
# 
# The dataset was checked for missing values, duplicate
# country-year records, and incorrect data types.
# 
# Numerical columns were converted to numeric formats,
# and invalid measurements were excluded.
# 
# Potential outliers were not automatically removed because
# large differences in GDP and CO₂ emissions across countries
# are important to the research question.
# 
# The cleaned dataset will be used for the machine learning stage.

# ## Machine Learning Plan
# 
# ### Type of Machine Learning
# 
# I plan to use supervised machine learning, specifically
# regression models, to predict life expectancy based on
# GDP per capita and CO₂ emissions per capita.
# 
# I will initially use Linear Regression because it is
# simple, interpretable, and suitable for examining
# relationships between numerical variables.
# 
# I may also explore Random Forest Regression to capture
# potential nonlinear relationships.
# 
# ### Potential Challenges
# 
# 1. **Small Dataset:** The dataset contains approximately
#    70 observations across five countries, which may
#    limit model accuracy and generalization.
# 
# 2. **Different Economic Conditions:** Countries have
#    significantly different GDP levels, which may
#    influence predictions.
# 
# 3. **Correlation vs. Causation:** Relationships between
#    GDP, emissions, and life expectancy do not establish
#    cause and effect.
# 
# 4. **Overfitting:** A complex model may perform well
#    on training data but poorly on unseen observations.
# 
# ### How I Will Address These Challenges
# 
# - Use a simple Linear Regression model as a baseline.
# - Split data chronologically into training and testing
#   sets to avoid training on future observations.
# - Evaluate performance using MAE, RMSE, and R².
# - Consider scaling numerical features when appropriate.
# - Compare predictions with actual life expectancy values.
# - Interpret results carefully due to the small dataset
#   and differences between countries.

# ## Prior Feedback and Project Updates
# 
# ### Feedback Received
# 
# I reviewed my Checkpoint 1 project and considered
# the requirements for the next stage of analysis.
# 
# ### Changes Made Since Checkpoint 1
# 
# 1. Added exploratory data analysis and statistical summaries.
# 2. Examined missing values, duplicates, and data types.
# 3. Created four visualizations using Matplotlib and Seaborn.
# 4. Added data cleaning and transformation procedures.
# 5. Developed a supervised machine learning plan
#    using regression models.
# 
# ### Future Improvements
# 
# I plan to investigate correlations further, evaluate
# model performance, and explore whether GDP per capita
# and CO₂ emissions can help predict life expectancy.
