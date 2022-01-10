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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
timeout=10
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

	with open('output.txt',encoding="utf-8") as sf:
		surnocs = sf.readlines()
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	driver = webdriver.Chrome(options=options)  # os.path.join(os.curdir, 'chromedriver.exe'


	with open('output1.txt', 'w',encoding="utf-8") as of:
		# Loop survey
		for surnoc in surnocs:
			driver.get("http://landrecords.karnataka.gov.in/rtconline/")
			time.sleep(3)

			# Select district
			driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_District']/option[text()='" + district + "']").click()
			print('Select district: ', district)
			# WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By., "pt-collapse-list")))
			time.sleep(0.5)

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
			print('Trying for: ', surnoc.rstrip())
			surnoc = surnoc.rstrip().split(' ')
			driver.find_element_by_xpath("//input[@name='ctl00$MainContent$txtSurvey']").clear()
			time.sleep(2)
			driver.find_element_by_xpath("//input[@name='ctl00$MainContent$txtSurvey']").send_keys(surnoc[0])
			driver.find_element_by_xpath("//div[@class='footer']").click()
			success=False
			for i in range(5):
				try:
					time.sleep(2)
					driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_surnoc']/option[normalize-space()='" + surnoc[1] + "']").click()
					success=True
					break
				except:
					continue
			if not success:
				print("Skipping blank entry")
				continue
			success=False
			for i in range(5):
				try:
					time.sleep(2)
					driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddl_hissa']/option[normalize-space()='" + surnoc[2] + "']").click()
					success=True
					break
				except:
					continue
			if not success:
				print("Skipping blank entry")
				continue
			time.sleep(2)
			error_element = driver.find_element_by_xpath("//span[@id='ctl00_MainContent_lbl_error']")
			print(error_element.text)
			if len(error_element.text)>5:
				print("Skipping blank combination")
				continue
			else:
				driver.find_element_by_xpath("//input[@id='ctl00_MainContent_btnFetchDetails']").click()
				WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "__tab_ctl00_MainContent_Tabcontrol_TabPanel2")))
				driver.find_element_by_xpath("//a[@id='__tab_ctl00_MainContent_Tabcontrol_TabPanel2']").click()
				WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[@id='ownerdetails']/table")))
				soup=BeautifulSoup(driver.page_source,features="html.parser")
				span = soup.find("span",{"id":"ownerdetails"})
				table = span.findAll("table")[0]
				# print(table)
				trs = table.findAll("tr")
				# print(trs)
				for i in range(2,len(trs)):
					# print(trs[i])
					tds=trs[i].findAll("td")
					print(tds[0].text+":"+tds[1].text)
					of.write('{},{},{},{},{}\n'.format(surnoc[0], surnoc[1], surnoc[2],tds[0].text,tds[1].text))
					# print(trs[i][1])
				# break









if __name__ == '__main__':
	karnatakaScrape()
