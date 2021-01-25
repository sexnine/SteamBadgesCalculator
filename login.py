import yaml
import pickle
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

config = None


def load_config():
    print("Loading config")
    with open("config.yml", "r") as f:
        global config
        config = yaml.safe_load(f)
    print("Loaded config!")


class CheckLoggedIn(object):
    def __call__(self, driver):
        if driver.current_url.startswith("https://steamcommunity.com/id/"):
            return True
        try:
            return driver.find_element_by_id("auth_message_success").get_attribute("style") == ""
        except StaleElementReferenceException:
            return False


def main():
    load_config()
    driver = webdriver.Chrome(config.get("driver_file_path", "chromedriver.exe"))
    driver.get("https://steamcommunity.com/login/")
    print("Please sign into Steam, you have 180 seconds to do so.")

    try:
        WebDriverWait(driver, timeout=180, poll_frequency=1).until(CheckLoggedIn())
    except TimeoutException:
        print("You took too long to sign in (180 seconds)")
    print("Signed in!")
    pickle.dump(driver.get_cookies(), open("data/cookies.pkl", "wb"))
    print("Saved login data!")
    driver.quit()


if __name__ == "__main__":
    main()