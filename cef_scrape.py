import re
import csv
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

id = 0
list_dict = []
list_codes = []
current_date = date.today()
read_file = "cef_input.csv"

# open input file
with open(f'{read_file}', 'r', newline='') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        list_codes.append(row['code'])

driver = webdriver.Chrome()

for product_code in list_codes:
    # navigate to url
    driver.get(f"https://www.cef.co.uk/catalogue/products/search?q={product_code}")
    
    # wait for webpage elements to load
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='price']")))

    # get elements
    name_el = driver.find_element(By.TAG_NAME, "h3")
    price_el = driver.find_element(By.XPATH, "//span[@class='price']")

    # data
    id += 1
    name = name_el.text
    supplier = "CEF"
    price = int(re.sub(r'[^0-9]', '', price_el.text))/100 # regex filter price

    dict = {'ID': id, 'Item': name, 'Product Code': product_code, 'Supplier': supplier, 'Price Ex VAT': price}
    list_dict.append(dict)

keys = list_dict[0].keys()

with open(f'cef_output_{current_date}.csv', 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, keys)
    writer.writeheader()
    writer.writerows(list_dict)