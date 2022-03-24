from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

#Help to open Chrome browser using selenium
browser = webdriver.Chrome("/Users/ISHITA AGGARWAL/Downloads/chromedriver_win32/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []

def scrape():

    for i in range(0,201):

        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):

            li_tags = ul_tag.find_all("li")
            temp_list = []

            #iterating all li tags
            #both index and data
            for index,li_tag in enumerate(li_tags):

                if index == 0:
                    #fetching data of 0 index
                    #finding first anchor tag(a)
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    #Will not append anything
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)

        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,"html.parser")
    temp_list = []
    for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
            except:
                temp_list.append("")
        new_planet_data.append(temp_list)

scrape()

for data in planet_data:
    scrape_more_data(data[5])
 
final_planet_data = []
for index, data in enumerate(planet_data):
    final_planet_data.append(data + final_planet_data[index])

#save data
with open("final.csv", "w") as f:

    #write data inside file
    csvwriter = csv.writer(f)
    #what all to write
    csvwriter.writerow(headers)
    #under headers save data
    csvwriter.writerows(planet_data)
