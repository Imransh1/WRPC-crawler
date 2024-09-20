from selenium import webdriver
from time import sleep
import warnings
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.keys import Keys
import traceback
from paths import driver_path
from crawler import wrpc_crawler
from selenium.webdriver.chrome.service import Service


def main():

    try:
        URL = "https://www.wrpc.gov.in/index.html"
        
        Webdriver_Service = Service(executable_path=driver_path)
        # warnings.filterwarnings('ignore')

        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36'
        ]

        user_agent = random.choice(user_agent_list)
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("window-size=1900,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, service=Webdriver_Service)
        
        driver.get(URL)

    except:
        print(traceback.format_exc())
    
    wrpc_crawler(driver)


if __name__ == "__main__":
    main()
