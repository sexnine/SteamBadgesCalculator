import yaml
import pickle
from selenium import webdriver
import time
import math


config = None


def load_config():
    print("Loading config")
    with open("config.yml", "r") as f:
        global config
        config = yaml.safe_load(f)
    print("Loaded config!")


def generate_html(badges: list):
    template = """
    <head>
        <style>
            table, th, td {
                border: 1px solid black;
                font-family: Arial,serif;
            }
            table {
                margin: 20px;
            }
            td {
                padding: 10px;
            }
            th {
                font-size: 24px;
                padding: 10px;
            }
            a {
                color: black;
            }
            a:hover {
                color: deepskyblue;
            }
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Price</th>
                <th>Name</th>
            </tr>
            {tabledata}
        </table>
    </body>
    """
    table_data = ""
    for badge in badges:
        table_data += f"<tr><td>{badge['price']}</td><td><a href='{badge['link']}'>{badge['title']}</a></td><tr>"

    return template.replace("{tabledata}", table_data, 1)


def main():
    start_time = time.time()
    load_config()
    driver = webdriver.Chrome(config.get("driver_file_path", "chromedriver.exe"))
    badge_links = []
    badges = []

    print("Loading home page")
    driver.get("https://steamcommunity.com")
    print("Adding cookies and refreshing page")
    try:
        cookies = pickle.load(open("data/cookies.pkl", "rb"))
    except FileNotFoundError:
        print("Couldn't find cookies, was it deleted?  Run login.py to login before running this file.")
        driver.quit()
        exit(0)

    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://steamcommunity.com/?l=english")

    print("Getting list of all badges...")
    try:
        driver.get(driver.find_elements_by_xpath("//*[contains(text(), 'View profile')]")[0].get_attribute("href") + "badges/?l=english")
    except:
        print("Couldn't navigate to your badges...  Are you logged in?  Make sure to log in using login.py")
        driver.quit()
        exit(0)

    badge_elements = driver.find_elements_by_class_name("badge_row")
    print(f"Found a total of {str(len(badge_elements))} badges.  Narrowing it down to uncompleted badges with no card drops remaining.")

    err = 0
    for badge in badge_elements:
        try:
            if badge.find_element_by_class_name("progress_info_bold").text != "No card drops remaining":
                continue
            badge_link = badge.find_element_by_class_name("badge_row_overlay").get_attribute("href")
            badge_links.append(badge_link + "?l=english")
        except:
            err += 1
            continue

    print(f"Narrowed it down to {str(len(badge_links))} badges.")

    counter = 0
    for badge_link in badge_links:
        counter += 1
        print(f"Getting data from {badge_link}. {str(counter)}/{str(len(badge_links))}")
        tries = 0
        for i in range(2):
            try:
                driver.get(badge_link)
                a = driver.find_elements_by_class_name("gamecards_inventorylink")[1]
                buy_link = a.find_element_by_class_name("btn_grey_grey").get_attribute("href")
                badge_title = driver.find_element_by_class_name("badge_title").text

                driver.get(buy_link)
                price = driver.find_element_by_id("market_multibuy_order_total").text
                badges.append({"link": badge_link, "price": price, "title": badge_title})
                break
            except:
                tries += 1
                if tries >= 2:
                    print(f"Failed getting data from {badge_link} 2 times... Skipping and moving onto the next one in 5 seconds...")
                else:
                    print(f"Got an error while getting data from {badge_link}.  Trying again in 5 seconds...")
                time.sleep(5)

    print("Gathered all data!  Sorting and writing results to a file.")

    driver.quit()

    final_badges_list = sorted(badges, key=lambda k: k['price'])
    html = generate_html(final_badges_list)
    with open("results.html", "w") as f:
        f.write(html)

    byebye = f"""

Done! Completed in {math.floor(time.time() - start_time)}s
You can see the results by opening results.html in your web browser.
Know any ways this can be improved?  Open an issue on Github!  I'd love to hear your feedback :)
-sexnine (https://github.com/sexnine/SteamBadgesCalculator)
    """

    print(byebye)


if __name__ == "__main__":
    main()
