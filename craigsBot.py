import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from os import path
from authenticate import twitter

# User search parameters
city = 'vancouver'
minPrice = '5000'
maxPrice = '25000'
mileage = '100000'
keyWords = ['lexus', 'infiniti', 'acura', 'bmw', 'mercedes', 'audi', 'volkswagen']

# Chrome driver configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("--disable-dev-shm-usage")

# Get listings from craigslist
def getListings(browser):
    
    listings_full = browser.find_elements(By.CLASS_NAME, 'result-row')
    listings_refined = []
    
    # Get first 25 listings
    for index, listing in enumerate(listings_full):
        if(index > 24): break 
        # Store desired listing info
        info = {
            "title": listing.text[:listing.text.rfind('$')], 
            "url": listing.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        }

        listings_refined.append(info)

    return listings_refined

# refresh listings from craigslist
def refresh(browser, listings):
    
    browser.refresh()
    sleep(30)
    newListings = browser.find_elements(By.CLASS_NAME, 'result-row')
    
    for index, newListing in enumerate(newListings):
        if(index > 24): break
        # Update with new listings
        listings[24 - index]['title'] = newListing.text[:newListing.text.rfind('$')]
        listings[24 - index]['url'] = newListing.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')


def main():
    # Build url for craigslist search
    url = 'https://' \
          + city + \
          '.craigslist.org/d/cars-trucks/search/cta?max_auto_miles=' \
          + mileage + \
          '&max_price=' \
          + maxPrice + \
          '&min_price=' \
          + minPrice

    # Start chrome driver
    browser = webdriver.Chrome(
        service=Service(path.join(sys.path[0], 'chromedriver')), 
        options=chrome_options
    )

    browser.get(url)
    listings = getListings(browser)

    while True:
        
        # Refresh and retrieve new listings
        refresh(browser, listings)

        # Filter listings and log viewed listings
        for listing in listings:
            if any(keyWord in listing['title'].lower() for keyWord in keyWords):
                with open(path.join(sys.path[0], 'listings.log')) as rFile:
                    if listing['url'] not in rFile.read():

                        wFile = open(path.join(sys.path[0], 'listings.log'), mode='a')
                        wFile.write(listing['url'] + '\n')
                        wFile.close()
                        messege = listing['title'] + '\n' + listing['url'] + '\n'
                        # Send listing as direct message to twitter user
                        twitter.send_direct_message(twitter.get_user(screen_name='username here').id_str, messege)

        sleep(600)

if __name__ == "__main__":

    main()