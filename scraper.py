import os
import re
import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def make_request(url, make_soup=True):
        r = requests.get(url)
        if r.status_code != 200:
            print(r.status_code, url)

        if make_soup:
            return BeautifulSoup(r.content, 'html.parser')

        return str(r.content)


def karnatakaScrape():

    with open('config.json') as cf:
        config = json.load(cf)

        district = config['district']
        taluk = config['taluk']
        hobli = config['hobli']
        village = config['village']

    with open('survey.txt') as sf:
        surveys = sf.readlines()

    driver = webdriver.Chrome()  # os.path.join(os.curdir, 'chromedriver.exe'
    driver.get("http://landrecords.karnataka.gov.in/rtconline/")
    time.sleep(3)

    # Select district
    driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_District']/option[text()='" + district + "']").click()
    print('Select district: ', district)
    time.sleep(2)

    # Select taluk
    driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_Taluk']/option[text()='" + taluk + "']").click()
    print('Select taluk: ', taluk)
    time.sleep(2)

    # Select hobli
    driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_Hobli']/option[text()='" + hobli + "']").click()
    print('Select hobli: ', hobli)
    time.sleep(2)

    # Select village
    driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_Village']/option[text()='" + village + "']").click()
    print('Select village: ', village)
    time.sleep(2)

    with open('output.txt', 'w') as of:
        # Loop survey
        for survey in surveys:
            print('Survey: ', survey)        
            driver.find_element_by_xpath("//input[@name='ctl00$MainContent$txtSurvey']").clear()
            time.sleep(1)
            driver.find_element_by_xpath("//input[@name='ctl00$MainContent$txtSurvey']").send_keys(survey)
            time.sleep(3)

            surnoc_select = Select(driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_surnoc']"))
            surnoc_elements = surnoc_select.options

            for surnoc_element in surnoc_elements:
                surnoc = surnoc_element.text
                if surnoc != '-Select-':
                    print('Surnoc: ', surnoc)
                    driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_surnoc']/option[text()='" + surnoc + "']").click()
                    time.sleep(2)
                    
                    hissa_select = Select(driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_hissa']"))
                    hissa_elements = hissa_select.options

                    for hissa_element in hissa_elements:
                        hissa = hissa_element.text
                        if hissa != '-Select-':
                                print('Hissa: ', hissa)
                                of.write('{} {} {}\n'.format(survey, surnoc, hissa))


if __name__ == '__main__':
    karnatakaScrape()
