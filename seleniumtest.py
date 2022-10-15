from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Safari()
#action = ActionChains(driver)

driver.get("https://google.com/")

try:
    element = driver.find_element(By.NAME, "q")
except:
    print('Not found')

element.send_keys('Ya.ru', webdriver.Keys.ENTER)

