# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

def scrap_latlon(location):
    '''
    The Function returns the latitude and longitude from Google Maps
    
    Imput: location
    
    Output: tuple Latitude and longitude
    '''
    # options and open the driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options = options)
    # open the URL
    driver.get('https://www.google.com/maps')
    
    # Search the box input and send the location
    box_input = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    box_input.send_keys(location)
    
    # Search the button search and then click
    button_search = driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
    button_search.click()
    
    # after the search, wait until the panel appers
    WebDriverWait(driver, 15).until(
        expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]')))
    
    # get the text to check 
    text_check = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]').text
    
    # check if the locations exists, else return nothing
    try:
        validation = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]')
    except:
        driver.close()
        return ()
    
    # if the location return Yucatán, return nothing
    if 'Yucatán' in text_check:
        driver.close()
        return ()
    
    # check if the location was found, return nothing
    if text_check == f'Google Maps no puede encontrar {location}':
        driver.close()
        return ()
    # else return the latitude and longitude
    else:
        time.sleep(1)
        current_url = driver.current_url
        lat_lon = current_url.split('/')[6].split(',')[:2]
        lat = lat_lon[0].replace('@','')
        lon = lat_lon[1]
        driver.close()
        return (lat,lon)