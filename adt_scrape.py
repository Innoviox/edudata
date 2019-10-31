import csv
from uszipcode import SearchEngine
from selenium import webdriver
import time
driver = webdriver.Chrome("./chromedriver")
URL = "https://www.adt.com/crime?{},{},15"
search = SearchEngine(simple_zipcode=True)

xpath = "/html/body/div[1]/div[2]/div[3]/div"

with open("adt.csv", "a+") as f:
    out = csv.DictWriter(f, fieldnames=["Zip", "Crime"])
    out.writeheader()
    linen = 0
    for line in csv.DictReader(open("edudata.csv")):
        linen += 1
        if linen < 349:
            continue
        code = line['Zip Code'].split("-")[0]
        zc = search.by_zipcode(code)
        driver.get(URL.format(zc.lat, zc.lng))
        driver.find_element_by_xpath(xpath).click()
        driver.find_elements_by_xpath(xpath)[0].click()
        time.sleep(2)
        data = {'Zip': code, 'Crime': 0}
        try:
            el = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/div[3]/div/div[4]/div/div/div/div/div/div/div/div/span[3]")
            _, _, _, _, rate, *_ = el.text.split()
            rate = float(rate[:-1])
            if rate < 1:
                rate = 1 - rate
            data['Crime'] = rate
            print(data) 
        except Exception as e:
            print(f"Couldn't find data for {code}: {e}")
        out.writerow(data)
