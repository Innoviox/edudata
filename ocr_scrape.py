from selenium import webdriver
from uszipcode import SearchEngine
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome("./chromedriver")

find = driver.find_element_by_xpath
name_in = "/html/body/form/div[2]/div[1]/div[1]/div[1]/fieldset[1]/table/tbody/tr[2]/td[1]/input"
zip_in = "/html/body/form/div[2]/div[1]/div[1]/div[1]/fieldset[1]/table/tbody/tr[3]/td[3]/input"
search_btn = "/html/body/form/div[2]/div[1]/div[1]/div[1]/fieldset[1]/table/tbody/tr[4]/td[2]/button"
results = "/html/body/form/div[2]/div[1]/div[1]/div[1]/fieldset[2]/table[2]/tbody/tr[1]"
export_btn = "/html/body/form/div[2]/div[1]/div[1]/div[1]/fieldset[2]/table[1]/tbody/tr[1]/td[2]/button"
error_msg = "/html/body/div[1]/div[2]/div"
close_btn = "/html/body/div[1]/div[2]/center/input"

search = SearchEngine(simple_zipcode=True)

for zc in search.by_state("florida", returns=-1):
    driver.get("https://ocrdata.ed.gov/DistrictSchoolSearch#schoolSearch")
    find(name_in).send_keys("\b\b\b\bhigh")
    find(zip_in).send_keys(f"\b\b\b\b\b{zc.zipcode}")
    find(search_btn).click()

    time.sleep(2)

    try:
        find(results)
        find(export_btn).click()
        print(f"successful export for zipcode {zc.zipcode}")
    except NoSuchElementException as nsee:
        print(f"error: did not find anything for zipcode {zc.zipcode}")
        print(f"error: {find(error_msg).text}")
        # find(close_btn).click()
        driver.execute_script("app.closeMessage()")
    
