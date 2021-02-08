# Python program to search Mercadolibre for the best deals on desired products using Selenium and Requests

# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
import requests
from bs4 import BeautifulSoup
from operator import attrgetter

# Product class for program
class Product:
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url
    
    def __getPrice__(self, price):
        return self.price

# Start function to open browser in Incognito Mode
def start():
    # Open Chrome Browser in INcognito Mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options = chrome_options)

    # Hide browser without minimizing
    # Note: browser.minimize_window() will cause program to stop going to next page
    browser.set_window_position(-2000, 0)

    browser.get('https://www.mercadolibre.com.mx/')

    return browser

# Function to search for item in Amazon
def search(productName, browser):
    productSearch = browser.find_element_by_xpath('/html/body/header/div/form/input')
    productSearch.send_keys(productName)
    searchButton = browser.find_element_by_class_name('nav-search-btn')

    browser.implicitly_wait(3)
    searchButton.click()

# Function to search for desired item in list
def findProduct(productName, browser):
    
    print('Searching for Products...')

    # Get individual keywords to compare product names and fiund relevant products
    nameKeyWords = productName.lower().split(' ')

    # Empty array to store Product objects
    products = []
    name = ''
    price = ''
    url = ''

    # Loop to iterate all result pages
    while True:
        try:
            # Get current result page data
            searchURL = browser.current_url
            searchPage = requests.get(searchURL)
            searchSoup = BeautifulSoup(searchPage.content, 'html.parser')

            listViewButton = browser.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/aside/section[1]/div[2]/div[2]/a[1]')
            listViewButton.click()
            
            results = searchSoup.findAll(class_='ui-search-result__wrapper')
           
            # Iterate through all results in page to find relevant produts
            for i in results:

                # Get name of product
                name = str(i.find(class_='ui-search-item__title'))
                name = name.replace('<h2 class="ui-search-item__title">', '')
                name = name.replace('</h2>','')
                name = name.replace('<h2 class="ui-search-item__title ui-search-item__group__element">','')
                
                # Split name to compare
                productNameKeys = name.replace('-',' ')
                productNameKeys = name.lower().split(' ')
                
                # Get price from HTML
                priceStr = str(i.find(class_='ui-search-item__group ui-search-item__group--price'))

                # Clean up Price data
                priceStr = priceStr.replace('<div class="ui-search-item__group ui-search-item__group--price"><div class="ui-search-price ui-search-price--size-medium ui-search-item__group__element"><div class="ui-search-price__second-line"><span class="price-tag ui-search-price__part"><span class="price-tag-symbol">$</span><span class="price-tag-fraction">','')
                priceStr = priceStr.replace(',','')
                priceStr = priceStr.replace('</span></span><span class="ui-search-price__second-line__label"></span></div></div></div>','')
                
                # Get product URL
                link = i.find('a').get('href')

                # Check if product is relevant to search
                validName = True
                for word in nameKeyWords:
                    if word not in productNameKeys:
                        validName = False

                # If product is relevant, add it to the list
                if validName is True:
                    products.append(Product(name, priceStr, link))
            
            # Travel to next result page
            try:
                nextPage = browser.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/section/div[2]/ul/li[4]')
            except selenium.common.exceptions.NoSuchElementException:
                nextPage = browser.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/section/div[2]/ul/li[3]')
            
            nextPage.click()
        
        # If last page is reached, print message to tell user
        except selenium.common.exceptions.ElementClickInterceptedException:
            print('Last page reached')
            print('\n\n')
            break
    
    return products
    

# Method to sort products by Price
def sortProducts(products):
    sortedProducts = sorted(products, key = attrgetter('price'))

    return sortedProducts


# Function to print Product data
def printProducts(products):
    print('Products List')
    print('______________\n\n')

    # Checks if product list is empty, if so tells user
    if not products:
        print('No products found')

    # Prints Product data
    else:
        cont = 1
        for product in products:
            print(f'Product {cont}')
            print(f'Name: {product.name}')
            print(f'Product Price: ${product.price}')
            print(f'Product URL: {product.url}')
            print('')

            cont +=1
    

# Method to run program multiple times
def run():
    productName = input('What product do you wish to search for?: ')

    browser = start()

    page = 0

    search(productName, browser)
    products = findProduct(productName, browser)

    products = sortProducts(products)

    printProducts(products)

    browser.quit()


# Infinite loop to run program
while True:
    run()
    print('')
    again = input('Search for another product? y/n: ')

    if again == 'n':
        break
