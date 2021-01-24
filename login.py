import pickle
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")

config = None

# Yes this was copy pasted was stack overflow because I couldn't be fucked to understand how to do it myself lmao
class wait_for_the_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False

def main():
    driver.get("https://steamcommunity.com/login/")

    try:
        WebDriverWait(driver, timeout=180, poll_frequency=1).until(wait_for_the_attribute_value((By.ID, "auth_message_success"), "style", ""))
    except TimeoutException:
        print("You took too long to sign in (180 seconds)")
    print("Signed in!")
    pickle.dump(driver.get_cookies(), open("data/cookies.pkl", "wb"))
    print("Saved login data!")
    driver.quit()


if __name__ == "__main__":
    main()