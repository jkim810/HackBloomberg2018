from selenium import webdriver
import asyncio
import time


def log():
    DRIVER = './chromedriver'
    driver = webdriver.Chrome(DRIVER)
    driver.get('http://codebb.cloudapp.net/BaseInvaders.html')
    time.sleep(1)
    l = driver.execute_script("return state.mines")
    driver.quit()
    return l