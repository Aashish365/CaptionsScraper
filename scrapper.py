from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
PATH='C:\Program Files\chromedriver.exe'
import requests
driver=webdriver.Chrome(PATH)
url="https://turbofuture.com/internet/Short-Captions-for-Profile-Pictures"
driver.get(url)
driver.maximize_window()


# This function is for clicking event on interctable object in the page
def button_click(button):
    driver.execute_script("arguments[0].click();", button)


# This function gives us the list of urls
def get_urls(data):
    urls=[]
    for link in data:
         if ( link.get_attribute('href').find("Caption") or link.get_attribute('href').find("Captions") or link.get_attribute('href').find("Quotes") )!=-1:
                urls.append("https://turbofuture.com"+link.get_attribute('href'))
    return urls        

# # This code is for scraping the captions
def get_data(url_string):  
    captions=[]
    pg=requests.get(url_string)
    my_data=BeautifulSoup(pg.content, 'html.parser')
    my_data=my_data.find_all('ul')
    for ul in my_data:
        ul=ul.find_all('li')
        if(len(ul)>30):
            for li in ul:
                captions.append(li.text)
    return captions




#  This portio of code is for clicking the load more button 9 times
for i in range(9):
        load_more = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'm-component-footer--loader'))
        )
        button_click(load_more)
        
data = driver.find_elements(By.TAG_NAME,'phoenix-super-link') # this gives all the phoenix-super-link tag in the page
my_urls=get_urls(data)

my_captions=[]

for i in range (len(my_urls)):
    my_captions.append(get_data(my_urls[i]))



# Creating a .txt file and writing the captions over it
            
file = open('captions.txt','w',encoding="utf-8")
for obj in my_captions:
    for caption in obj:
        file.write(caption+"\n")
file.close()    
driver.quit()
