from bs4 import BeautifulSoup
import requests
import pandas as pd

# function to cleaning price
def parse_price(price_str):
    # print(price_str)
    price = price_str.replace("Rp", "").replace(".", "")
    # print(price)
    return price

def parse_keyword(keyword):
    # Initialize an empty string to store the result
    result = ""

    # Iterate through each character in the keyword
    for i in range(len(keyword)):
        char = keyword[i]
        # If the character is a space and the next character is a number, replace it with '%'
        if char == ' ':
            # Check if the next character exists and if it's a number
            if i < len(keyword) - 1 and keyword[i+1].isdigit():
                result += '%'
            else:
                result += '%20'
        else:
            result += char
    return result

## scraping function
def scrape(page, keyword):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/546.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language' : 'en-US,en:q-0.5',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Connection' : 'keep-alive'
    }
    ## Cleaning keyword
    data = parse_keyword(keyword)
    try:
        if page == 1:
            url = f'https://www.tokopedia.com/search?st=&q={data}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)

            data_titles = soup.find_all('div', class_='prd_link-product-name css-3um8ox')
            data_prices = soup.find_all('div', class_='prd_link-product-price css-h66vau')
            data_ratings = soup.find_all('span', class_='prd_rating-average-text css-t70v7i')

            scraping = {'Title': [], 'Price': [], 'Rating': [], 'Page': []}
            for title, price, rating in zip(data_titles, data_prices, data_ratings):
                # print("Title:", title.text.strip())
                # print("Price:", price.text.strip())
                # print("Rating:", rating.text.strip())
                # print()  # for spacing
                scraping['Title'].append(title.text.strip())
                scraping['Price'].append(
                    parse_price(
                        price.text.strip()
                        )
                    )
                scraping['Rating'].append(rating.text.strip())
                scraping['Page'].append(page)

        else:
            url = f'https://www.tokopedia.com/search?navsource=&page={page}&q={data}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st='

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)

            data_titles = soup.find_all('div', class_='prd_link-product-name css-3um8ox')
            data_prices = soup.find_all('div', class_='prd_link-product-price css-h66vau')
            data_ratings = soup.find_all('span', class_='prd_rating-average-text css-t70v7i')

            scraping = {'Title': [], 'Price': [], 'Rating': [], 'Page': []}
            for title, price, rating in zip(data_titles, data_prices, data_ratings):
                # print("Title:", title.text.strip())
                # print("Price:", price.text.strip())
                # print("Rating:", rating.text.strip())
                # print()  # for spacing
                scraping['Title'].append(title.text.strip())
                scraping['Price'].append(
                    parse_price(
                        price.text.strip()
                        )
                    )
                scraping['Rating'].append(rating.text.strip())
                scraping['Page'].append(page)

    except requests.exceptions.RequestException as e:
        print("HTTP requests error :", str(e))
    except requests.exceptions.HTTPError as e:
        print("HTTP response error", str(e))
    finally:
        print(f"Sucess scraping from page {page}")
        print(len(scraping['Title']), 'Items')
        return scraping

def app():
    ## web scraping looping
    print("Initializing Web Scraping Application")
    print()
    keyword = str(input("Input keyword to scrape:"))
    i = 1
    pageLimit = int(input("Input page limit:"))
    print()

    ## Checking page limit
    if pageLimit < 1:
        print("Scrape app needs more than 0 pages")
    else:
        pass

    result = {'Title': [], 'Price': [], 'Rating': [], 'Page': []}
    while i <= pageLimit:
        data = scrape(i, keyword)
        if data is not None:
            result['Title'].extend(data['Title'])
            result['Price'].extend(data['Price'])
            result['Rating'].extend(data['Rating'])
            result['Page'].extend(data['Page'])
        else:
            print(f'Page {i} error scraping function')
        i += 1

    print()
    print(f"Sucess scraping {i-1} pages")
    print('Data details:')
    print('total', len(result), 'Items')
    print('total', len(result['Title']), 'Title')
    print('total', len(result['Price']), 'Price')
    print('total', len(result['Rating']), 'Rating')
    print('total', len(result['Page']), 'Pages')
    print()
    # print(result)

    ## Input data into dataframe
    df = pd.DataFrame.from_dict(result)
    # print(df)
    df.to_csv(f'{keyword}_{pageLimit} Pages_result.csv', index=False)
    print(f"Data export to directory with filename '{keyword}_{pageLimit} Pages_result.csv'")
    print()

while True:
    user_input = input("Do you want to scrape data? (y/n): ").lower()
    print()
    if user_input == 'y' or user_input == 'Y' :
        app()
    elif user_input == 'n' or user_input == 'N':
        print("Exiting.")
        break
    else:
        print("Invalid input! Please enter 'y' or 'n'.")
        print()