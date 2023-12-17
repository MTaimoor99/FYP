# A file containing helper functions for our views
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_reviews(product_url):
    #path='C:\\Users\\92317\\Downloads\\chromedriver-win64\\chromedriver.exe'
    path = '/usr/bin/chromedriver-linux64/chromedriver'
    chrome_path='/usr/bin/google-chrome'
    filename='daraz_reviews.csv'
    #open the browser
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()
    options.binary_location=chrome_path
    options.add_argument("start-maximized") #open Browser in maximized mode
    options.add_argument("disable-infobars") # disabling infobars
    options.add_argument("--disable-extensions") # disabling extensions
    options.add_argument("--disable-gpu") # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    browser.get(product_url)
    browser.maximize_window()
    Y=500 #Vertical distance to scroll by
    browser.execute_script(f"window.scrollTo(0,{Y})")
    #input_div=browser.find_element(By.CLASS_NAME,"content")
    #print(input_div)

    #Xpath=//div[@class="content"]
    #input_div=browser.find_element(By.XPATH, '//div[@class="content"]')
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    reviews=[]
    fieldname=['Reviews']
    with open(filename, 'w',encoding="utf-8") as file: 
        dw = csv.DictWriter(file, delimiter=',',  
                            fieldnames=fieldname) 
        dw.writeheader() 
    total_pages=int(WebDriverWait(browser, 60,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,'(//a[@rel="nofollow"])[last()]'))).text)
    for k in range(0,total_pages):
        if k==total_pages:
            break
        element=WebDriverWait(browser, 60,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,'//div[@class="review-content-sl"]')))
        next_button=WebDriverWait(browser, 60,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,'(//button[@class="ant-pagination-item-link"])[2]')))
        for i in range(1,4):  
            #input_div=browser.find_element(By.XPATH, f'(//div[@class="content"])[{i}]')
            input_div=WebDriverWait(browser, 60,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,f'(//div[@class="review-content-sl"])[{i}]')))
            if input_div.text=="":
                break
            with open(filename,'a',encoding='utf-8',errors='replace',newline='') as csvfile:
                csvwriter=csv.writer(csvfile)
                reviews.append(input_div.text)
                csvwriter.writerow(reviews)  
                reviews=[]
        next_button.click()
        time.sleep(2)
        browser.execute_script(f"window.scrollTo(0,{Y-100})")
    browser.quit()


