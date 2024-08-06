import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class MobalyticsScraper:
    def __init__(self):
        self.options = self._configure_options()
        self.driver = self.initialize_driver()
        # We create an instance of WebDriverWait with the maximum wait time as 10 seconds. 
        # Once expected condition is met while fetching current patch returned we will continue.
        self.wait = WebDriverWait(self.driver, 10)
        # Load environment variables from a .env file
        load_dotenv()

    def _configure_options(self):
        # We set options of the browser which we are going to use.
        options = webdriver.ChromeOptions()
        # We will use headless mode to not open the browser by adding headless flag to options of browser.
        options.add_argument("--headless")
        # We disable sandbox which is OS security model reducing performance and may cause crash during testing.
        options.add_argument("--no-sandbox")
        # We use disable-dev-shm-usage flag to overcome limited resource problems by disabling using of /dev/shm
        # shared memory file system which may reduce memory usage and causing Chrome to fail or crash during testing.
        options.add_argument("--disable-dev-shm-usage")
        return options
    # Initialize driver of Chrome browser with options that we set.
    def initialize_driver(self):
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=self.options
        )

    def fetch_champion_data(self, champion_name):
        print(f"Fetching {champion_name.lower().capitalize()}\n")
        # We manage input.
        champion_name = champion_name.lower()
        champion_name = champion_name.replace(" ", "")
        # We fetch champion page and we are ready to use code in our headless browser.
        self.driver.get(f"https://mobalytics.gg/lol/champions/{champion_name}/build")

        try:
            data = {
                'current_patch': self.get_text(os.getenv("CURRENT_PATCH_XPATH")),
                'win_rate': self.get_text(os.getenv("WIN_RATE_XPATH")),
                'runes1_title': self.get_text(os.getenv("RUNES1_TITLE_XPATH")),
                'runes2_title': self.get_text(os.getenv("RUNES2_TITLE_XPATH")),
                'runes1': self.get_runes(os.getenv("RUNES1_XPATH")),
                'runes2': self.get_runes(os.getenv("RUNES2_XPATH")),
                'other_attributes': self.get_elements(os.getenv("OTHER_ATTRIBUTES_XPATH"), "m-1u3ui07"),
                'build': self.get_elements(os.getenv("BUILD_XPATH"), "m-5o4ika"),
                'ability_order': self.get_ability_order(os.getenv("ABILITIES_XPATH")),
            }
        except Exception as e:
            data = {}
            print(f"Error occurred: {e}")

        return data

    # We use get_text function to get texts for patch, win rate, titles.
    def get_text(self, xpath):
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element.text

    # We use get_runes function to get runes of champion.
    def get_runes(self, xpath):
        elements = self.driver.find_elements(By.XPATH, xpath)[0]
        runes = [rune.get_attribute("alt") for rune in elements.find_elements(By.CLASS_NAME, "m-1nx2cdb")]
        if xpath == os.getenv("RUNES1_XPATH"):
            runes = [elements.find_elements(By.CLASS_NAME, "m-1iebrlh")[0].get_attribute("alt")] + runes
        return runes       

    # We use get_elements function to get other elements of champion like build items and other attributes.
    def get_elements(self, xpath, class_name):
        elements = self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.CLASS_NAME, class_name)
        return [element.get_attribute("alt") for element in elements]

    # We use get_ability_order function to get ability order of champion.
    def get_ability_order(self, xpath):
        elements = self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.CLASS_NAME, "m-1p6spxi")
        abilities = list(enumerate([ability.text for ability in elements], 1))
        return self.edit_ability_order(abilities)
    
    # We use edit_ability_order function to edit ability order of champion.
    def edit_ability_order(self, abilities):
        # Our ability list is like [(1, 'Q'), (2, 'W'), (3, 'E'), (4, 'Q'), (5, 'Q')]
        # We need to print 4-5 Q instead of 4 Q 5 Q so we need to group ability keys with their orders if they are same consequtively.
        # Current order and key are the first element of the list.
        current_order = abilities[0][0]
        current_key = abilities[0][1]
        # We create a string to store the ability order string.
        ability_order_str = f"{current_order}"
        # We iterate each ability to group them by their orders.
        for i in range(1, len(abilities)):
            # If current key is same with iteration key we add -order to the string.
            if current_key == abilities[i][1]:
                ability_order_str += f"-{abilities[i][0]}"
            # If current key is different with iteration key we add space and current key to the string.
            # Then we update current order and key to the iteration order and key.
            # We add new line and current order which is iteration order to the string.
            else:
                ability_order_str += f" {current_key}"
                current_order = abilities[i][0]
                current_key = abilities[i][1]
                ability_order_str += f"\n{current_order}"
        # If for loop ends we add last key to the string.
        # Then we check if last key is same with current key if its not we add new line and last abilities order and key to the string.
        # Because if its same we already added it to the string. But we didnt add last ability key to the string.
        # But we add last ability key to the string when loop is over.
        ability_order_str += f" {current_key}"
        if current_key != abilities[-1][1]:
            ability_order_str += f"\n{abilities[-1][0]} {abilities[-1][1]}"
        return ability_order_str

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    # We create instance of MobalyticsScraper class.
    scraper = MobalyticsScraper()
    while True:
        # Getting input from user and setting the champion name to fetch.
        champion_name = input("Enter the champion you want to fetch: ")
        data = scraper.fetch_champion_data(champion_name)
        if data:
            print(f"Current patch: {data['current_patch']}")
            print(f"Win rate: {data['win_rate']}")

            print("\n--- RUNES ---")
            print(f"# {data['runes1_title'].upper()} #")
            for rune in data['runes1']:
                print(rune)
            print(f"# {data['runes2_title'].upper()} #")
            for rune in data['runes2']:
                print(rune)

            for attr in data['other_attributes']:
                print(attr)

            print("\n--- BUILD ---")
            for item in data['build']:
                print(item)

            print("\n--- ABILITY ORDER ---")
            print(data['ability_order'])

