# Julian Kropp, 2022
# using csv to store data information, BeautifulSoup for Webscraping and requests for html requests
import csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime


# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()

    except AttributeError:
        price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:

        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = ""

    return available


if __name__ == '__main__':
    # Headers for request
    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
                'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.de/Barilla-Pasta-Penne-Rigate-1kg/dp/B07YQG4M4D/ref=sr_1_6?__mk_de_DE=ÅMÅŽÕÑ&crid=17RV2UXEXNLHH&keywords=nudeln&qid=1663794060&rdc=1&sprefix=nudeln%2Caps%2C101&sr=8-6"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    current_day = datetime.today().strftime('%d-%m-%Y')

    # Function calls to display all necessary product information
    print("Product Title =", get_title(soup))
    print("Product Price =", get_price(soup))
    print("Product Rating =", get_rating(soup))
    print("Number of Product Reviews =", get_review_count(soup))
    print("Availability =", get_availability(soup))

    # write product information into a csv file for data handling
    with open("products.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([get_title(soup), current_day, get_price(soup), get_rating(soup), get_review_count(soup), get_availability(soup)])
    file.close()
