import pandas as pd

def get_data_by_location(df, location, columns=1):
    location = location.strip().lower()
    filtered_data = df[df['location'].str.contains(location, case=False, na=False)]

    if filtered_data.empty:
        return f"No data found for location: {location}"
    if columns == 1:
        return filtered_data
    elif columns == 2:
        return filtered_data['firm_name']
    else:
        return "Invalid option. Use 1 for all columns, 2 for firm names."