from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time as tm


def get_all_cars(html_soup):
    cars = []
    all_rows_in_html_page = html_soup.findAll('div', {'class': "row listing listing-plus bb-listing-clickable"})
    for table_row in all_rows_in_html_page:
        car_name = table_row.findAll('a', {'class': "listing-heading darkLink"})
        variable_data_column = table_row.findAll('span', {'class': "variableDataColumn"})
        listing_data = table_row.findAll('div', {'class': "col-xs-2 listing-data "})
        price = table_row.findAll('div', {'class': "col-xs-3 listing-price "})

        car_entry = {
            "car_name": car_name[0].text,
            "km_pr_liter": variable_data_column[0].attrs[u'data-kml'],
            "horsepower": variable_data_column[0].attrs[u'data-hk'],
            "km/t": variable_data_column[0].attrs[u'data-kmt'],
            "km_driven": listing_data[1].text,
            "year": listing_data[2].text,
            "price": price[0].text
        }
        cars.append(car_entry)
    return cars

cars_list = []
# (1, 200) = 5500 rows of data
for i in range(1201, 1500):
    html = urlopen("https://www.bilbasen.dk/brugt/bil?Fuel=0&YearFrom=0&YearTo=0&PriceFrom=0&PriceTo="
                   "10000000&MileageFrom=-1&MileageTo=10000001&IncludeEngrosCVR=true&IncludeLeasing=false&page=" + str(i))
    html_soup = BeautifulSoup(html, 'html.parser')
    cars_list += get_all_cars(html_soup)
    print(i)
    print(len(cars_list))
    tm.sleep(0.5)


df = pd.DataFrame(cars_list)
df.to_csv("bilbasen5.csv", sep=";")
print(df.head(5))
