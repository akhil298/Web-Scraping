import pandas as pd
from data_cleaning import clean_data
from data_extraction import scrape_data
from data_processing import get_data_by_location

# Paths
cleaned_data_path = 'cleaned_data.csv'
scraped_data_path = 'scraped_data.csv'

# Data Cleaning

raw_data = scrape_data("https://www.goodfirms.co/supply-chain-logistics-companies", scraped_data_path)

cleaned_df = clean_data(raw_data)


df = pd.read_csv(cleaned_data_path)
location = input("Enter location: ")
option = int(input("Enter 1 for all columns, 2 for firm names: "))
result = get_data_by_location(df, location, columns=option)

if isinstance(result, pd.DataFrame):
    print(result)
elif isinstance(result, pd.Series):
    print(result.to_string(index=False))
else:
    print(result)