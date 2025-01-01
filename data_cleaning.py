import pandas as pd
import numpy as np
import re

def clean_data(df):
    df.replace(['NA', 'N/A'], np.nan, inplace=True)
    
    # Fill missing values
    for column in df.select_dtypes(include=['object']).columns:
        df[column].fillna('Unknown', inplace=True)
    
    for column in df.select_dtypes(include=[np.number]).columns:
        df[column].fillna(np.nan, inplace=True)
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Normalize price
    def convert_price(value):
        if isinstance(value, str):
            value = re.sub(r'[^0-9.]', '', value)
            try:
                return float(value)
            except ValueError:
                return np.nan
        return value
    
    df['price'] = df['price'].apply(convert_price)
    
    # Normalize text data
    def normalize_text(text):
        if isinstance(text, str):
            text = text.lower()  # Convert text to lowercase
            text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove non-alphanumeric characters
        return text

    df['firm_name'] = df['firm_name'].apply(normalize_text)
    df['location'] = df['location'].apply(normalize_text)
    df['rating'] = df['rating'].apply(normalize_text)
    
    # Capitalize firm names
    df['firm_name'] = df['firm_name'].str.capitalize()
    
    # Additional normalization
    df['team_size'] = df['team_size'].str.strip()

    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Save cleaned data
    df.to_csv('cleaned_data.csv', index=False)
    print("cleaned_datas.csv saved!")
    
    return df