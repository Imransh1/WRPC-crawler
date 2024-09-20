import os
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import traceback
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import requests
import pdfplumber
from io import BytesIO
import pandas as pd
# from paths import driver_path

def wrpc_crawler(driver):

    action = ActionChains(driver)

    crawl_category_and_sub_category(driver,action)
    crawl_all_years(driver,action)
    crawl_weeks(driver,action)
    # sleep(2)
    # driver.quit()
    
        

def crawl_category_and_sub_category(driver,action):
        try:
            sleep(3)

            list_of_category_elements = driver.find_elements('xpath',"//a[@target='_parent']")
            print(f"Found: {len(list_of_category_elements)} Category Elements")
            for index,category_element in enumerate(list_of_category_elements):
                
                if index == 4: #move to 5 element i.e commercial.
        
                    action.move_to_element(category_element).perform()
                    sleep(1)

                    DSM_UI_account = driver.find_element('xpath',"//div[@id='menuItemHilite7']")
                    action.move_to_element(DSM_UI_account).perform()

                    if DSM_UI_account.is_displayed():

                        action.move_to_element(DSM_UI_account).click().perform()
        
                    break
        except:
            print("Error Finding Category/Subcategory Elements...\n", traceback.format_exc())

def crawl_all_years(driver,action):
        try:
            
            table = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//li[contains(@class, 'nav-item')]")))  
            if table:
                for year in table:
                    print(year.text)
                    year.click()
                    break
            else:
                print("No table found")  
        except:
            print("Error finding years\n", traceback.format_exc())

def crawl_weeks(driver,action):
        try:
            sleep(2)
            tr_elements = driver.find_elements(By.XPATH,"//tr[@colspan='2']")
            print(f"Found: {len(tr_elements)} Week Elements")
            
            original_window = driver.current_window_handle
            for index, tr in enumerate(tr_elements):
                
                action.move_to_element(tr).perform()
                sleep(2)
                week = tr.find_element(By.TAG_NAME, 'span') #"//span[contains(text(), 'week')]"
                action.move_to_element(week).perform()
                sleep(1)
                week.click()
                sleep(2)

                new_window = [ handle for handle in driver.window_handles if handle != original_window ][0]
                driver.switch_to.window(new_window)
                
                scrape_pdfs(driver,index)

                driver.close()
                driver.switch_to.window(original_window)

                # if index == 1:
                #      break
        
        except:
            print("Error finding weeks\n", traceback.format_exc())

def scrape_pdfs(driver,index):
    current_url = driver.current_url
    print("Current URL:", current_url)

    response = requests.get(current_url)

    data = []

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        
        for this_index,page in enumerate(pdf.pages):
                if this_index >19:
                    break
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if len(row)==7 and row[1] == 'TPCL_Mundra':    
                            print(row)
                            data.append(row)
    header = ['Date', 'Entity', 'Injection', 'Schedule', 'DSM Payable', 'DSM Receivable', 'Net DMC']
    
    df = pd.DataFrame(data, columns=header)
    df.to_csv(f'Output-{index+1}.csv', index=False)

