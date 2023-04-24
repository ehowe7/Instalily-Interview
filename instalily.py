import requests
from bs4 import BeautifulSoup

# function to scrape sitemap URLs from J.Crew website
def get_sitemap_urls():
    sitemap_url = 'https://www.jcrew.com/sitemap-wex/sitemap-index.xml'
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')
    urls = []
    prices = []

    
    # get all product categories from sitemap
    for url in soup.find_all('loc'):
        
        url_text = url.text.split('>')[0]
        if 'categories' in url_text:
            categories = requests.get(url_text)
            more = BeautifulSoup(categories.text, 'xml')

            #scan each category page for niche category
            for category in more.find_all('loc'):
                category_text = category.text.split('>')[0]
                products = requests.get(category_text)
                products_page = BeautifulSoup(products.text, 'xml')

                
                #scan each real category page for each product
                for each in products_page.find_all('div', {'class': 'ProductTile__content___jMoJD'}) :
                    for product in each.find_all('a', href=True):
                        product_url = product['href']
                        product_url = 'https://www.jcrew.com/' + product_url
                        

                        if product.find('div', {'class': 'tile__detail tile__detail--price ProductPrice__price___uYbqO'}) != None:
                            price = product.find('div', {'class': 'tile__detail tile__detail--price ProductPrice__price___uYbqO'}).text
                            prices.append(price)
                            urls.append(product_url)
                        

        
    return urls, prices


# function to extract product details from PDPs
def get_product_details(url, price):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')

    #grab product name
    product_name = soup.find('h1', {'id': 'product-name__p'}).text.strip()


    #get product description
    product_description = soup.find('p', {'class': 'ProductDescription__intro___ZGbWh'}).text.strip()
    # print(product_description)


    return {'name': product_name, 'price': price, 'description' : product_description}

# main function to scrape sitemap and extract product details
def main():
    sitemap_urls, prices = get_sitemap_urls()
    products = {}
    for url, price in sitemap_urls, prices:
        product_details = get_product_details(url, price)
        products[url] = product_details
    
    # chat repository to answer basic questions about products
    while True:
        user_input = input('What would you like to know about a product? ')
        if user_input == 'exit':
            break
        for url, product_details in products.items():
            if user_input in product_details['name'] or user_input in product_details['description']:
                print('Product Name:', product_details['name'])
                print('Product Price:', product_details['price'])
                print('Product Description:', product_details['description'])



main()

