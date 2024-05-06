# A file containing helper functions for our views
#All these below are needed to run our web scraper
import time
import csv
import os #Get the path of csv file using this module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException #For handling timeout exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#User login and sign up imports
from django.contrib.auth.forms import UserCreationForm

#to be used to generate pie plots
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import io #is used to write plot to a buffer
import base64 #is used to convert image to base64 format

def scrape_reviews(product_url):
    path='C:\\Users\\92317\\Documents\\7th Semester\\fyp_project\\chromedriver.exe'
    #path = '/usr/bin/chromedriver-linux64/chromedriver' #Uncomment for Docker
    #chrome_path='/usr/bin/google-chrome' #Uncomment for Docker
    filename='daraz_reviews.csv'
    #open the browser
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()
    #options.binary_location=chrome_path #uncomment for docker
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
        element=WebDriverWait(browser, 60,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,'//div[@class="review-content-sl"]')))
        if element is None:
            break
        if k==total_pages:
            break
        next_button=WebDriverWait(browser, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,'(//button[@class="ant-pagination-item-link"])[2]')))
        for i in range(1,4):  
            #input_div=browser.find_element(By.XPATH, f'(//div[@class="content"])[{i}]')
            try:
                input_div=WebDriverWait(browser, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH,f'(//div[@class="review-content-sl"])[{i}]')))
                if input_div.text=="":
                    break
                with open(filename,'a',encoding='utf-8',errors='replace',newline='') as csvfile:
                    csvwriter=csv.writer(csvfile)
                    reviews.append(input_div.text)
                    csvwriter.writerow(reviews)  
                    reviews=[]
            except TimeoutException:
                print("Element not found")
                break
        next_button.click()
        time.sleep(2)
        browser.execute_script(f"window.scrollTo(0,{Y-100})")
    browser.quit()
    current_dir=os.getcwd()
    csv_file_path=os.path.join(current_dir,filename)
    return csv_file_path   

def generate_pie_plot(predicted_sentiment_list):
        # Calculate counts of each category in predicted_sentiment_list
    counts = {
        'positive': predicted_sentiment_list.count('positive'),
        'negative': predicted_sentiment_list.count('negative'),
        'neutral': predicted_sentiment_list.count('neutral')
    }

    # Define colors for each category
    colors = {
        'positive': '#1f77b4',  # Blue
        'negative': '#ff7f0e',  # Orange
        'neutral': '#2ca02c'    # Green
    }

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%', colors=[colors[key] for key in counts.keys()])
    plt.title('Sentiment Insights')
    # Save the plot to a bytes object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the bytes object as a base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Close the plot to free memory
    plt.close()
    return image_base64




