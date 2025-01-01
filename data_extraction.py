import pandas as pd
from seleniumbase import SB,Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import numpy as np
import os

def scrape_data(url, output_path):
    driver = Driver(uc=True)
    
    all_firm_data = []
    current_page = 1

    while True:
        url = f"{url}?page={current_page}"
        print(f"Scraping page {current_page}...")
        
        try:
            # Open the URL
            driver.uc_open_with_reconnect(url, 4)
            
            driver.uc_gui_click_captcha()
            time.sleep(1)

            # Parse the page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all firm location blocks
            firm_blocks = soup.find_all('div', class_='firm-location custom_tooltip')

            # Loop through each firm block to extract details
            for firm_block in firm_blocks:
                # Extract firm location
                location_span = firm_block.find('span')
                firm_location = location_span.text.strip() if location_span else "N/A"

                # Find the closest preceding <h3> with class 'firm-name' for the firm name
                firm_name_h3 = firm_block.find_previous('h3', class_='firm-name')
                firm_name = firm_name_h3.find('a').text.strip() if firm_name_h3 else "N/A"

                # Find the closest rating-number
                rating_div = firm_block.find_next('div', class_='firm-rating js-modal-reviews')
                rating_span = rating_div.find('span', class_='rating-number') if rating_div else None
                firm_rating = rating_span.text.strip() if rating_span else "N/A"

                # Extract pricing, team size, and founded year
                firm_pricing = firm_block.find_previous('div', class_='firm-pricing custom_tooltip').find('span').text.strip() if firm_block.find_previous('div', class_='firm-pricing custom_tooltip') else "N/A"
                team_size = firm_block.find_previous('div', class_='firm-employees custom_tooltip').find('span').text.strip() if firm_block.find_previous('div', class_='firm-employees custom_tooltip') else "N/A"
                founded_year = firm_block.find_previous('div', class_='firm-founded custom_tooltip').find('span').text.strip() if firm_block.find_previous('div', class_='firm-founded custom_tooltip') else "N/A"

                # Append the extracted data to the list
                firm_data = {
                    "Firm Name": firm_name,
                    "Location": firm_location,
                    "Rating": firm_rating,
                    "Price": firm_pricing,
                    "Team Size": team_size,
                    "Founded": founded_year
                }
                all_firm_data.append(firm_data)
                print(firm_data)
            
            # Check if there is a "Next Page" button, if not, break the loop
            next_page_link = soup.find('li', class_='next-page')
            if not next_page_link or 'disabled' in next_page_link.get('class', []):
                print("No more pages to scrape.")
                break
            
            # Increment the page number for the next iteration
            current_page += 1

        except Exception as e:
            print(f"Error on page {current_page}: {e}")
            break

    # Close the browser
    driver.quit()

    # Convert the extracted data into a pandas DataFrame
    df = pd.DataFrame(all_firm_data)
    # os.makedirs(output_path,exist_ok=True)
    df.to_csv('Logistics.csv', index=False)
    print("Scraped........")
    
    return df


# scrape_data(url="https://www.goodfirms.co/supply-chain-logistics-companies",)