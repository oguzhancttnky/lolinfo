from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

while True:
    # We set options of the browser which we are going to use.
    options = webdriver.ChromeOptions()
    # We will use headless mode to not open the browser by adding headless flag to options of browser.
    options.add_argument("--headless")
    # We disable sandbox which is OS security model reducing performance and may cause crash during testing.
    options.add_argument("--no-sandbox")
    # We use disable-dev-shm-usage flag to overcome limited resource problems by disabling using of /dev/shm
    # shared memory file system which may reduce memory usage and causing Chrome to fail or crash during testing.
    options.add_argument("--disable-dev-shm-usage")
    # Setup of Chrome browser with options that we set.
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    # Getting input from user and setting the champion name to fetch.
    champion_name = input("Enter the champion you want to fetch: ")
    # We manage specific input cases.
    champion_name = champion_name.lower()
    champion_name = champion_name.capitalize()
    if champion_name == "Kaisa":
        champion_name = "Kai'Sa"
    elif champion_name == "Nunu":
        champion_name = "Nunu & Willump"
    elif champion_name == "Kogmaw":
        champion_name = "Kog'Maw"

    # We fetch website and we are ready to use code in our headless browser.
    driver.get("https://mobalytics.gg/lol/tier-list")
    print(f"Fetching {champion_name}\n")

    try:
        # We find the element of the champion with checking champion name by given input and get the link of that champion page.
        champion_element = driver.find_element(
            By.XPATH,
            f'//a[contains(@class, "m-ufpfcc") and .//span[contains(@class,"m-1hxcjhy") and text()="{champion_name}"]]',
        )
        champion_link = champion_element.get_attribute("href")
        # We navigate to the champion page by using the link of the champion by href.
        driver.get(champion_link)
        # We find current patch and win rate of the build of searched champion by getting text of their span elements.
        current_patch = driver.find_element(
            By.XPATH, "//div[contains(@class, 'm-1m86nuz')]"
        ).find_element(By.XPATH, ".//span")
        print(f"Current patch:{current_patch.text}")
        win_rate = driver.find_element(
            By.XPATH, "//div[contains(@class, 'm-1dp1qob')]"
        ).find_element(By.XPATH, ".//span")
        print(f"Win rate: {win_rate.text}")

        print("\n--- RUNES ---")
        # We find the rune title elements by using the class name.
        rune_titles = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'm-16mmcnu')]"
        )
        # We create a dictionary to store the runes with their titles as key and their names as value which is empty yet.
        runes = {rune_titles[0].text: [], rune_titles[1].text: []}
        # We find all rune elements by using the class name.
        rune_elements = driver.find_elements(
            By.XPATH, ".//div[contains(@class, 'm-ku03qt')]"
        )
        # We iterate each rune element to get names of the runes.
        for rune_element in rune_elements:
            # We find the parent element of the rune element to get the title of the rune.
            parent = rune_element.find_element(By.XPATH, "../..")
            rune_title = parent.find_element(
                By.XPATH, ".//div[contains(@class, 'm-swnc0e')]"
            )
            # We find all images of rune elements to get classnames and names of the runes by reaching alt tag of image.
            images = rune_element.find_elements(By.TAG_NAME, "img")
            runes_classnames_and_names = []
            # We iterate each image to get classname and name of the rune.
            for img in images:
                runes_classnames_and_names.append(
                    [img.get_attribute("class"), img.get_attribute("alt")]
                )
            # Different classname of between 3 runes is unique and we can get rune that user should use.
            # Our aim is to get that unique classname rune by checking classnames of 3 runes.
            for i, current_class in enumerate(runes_classnames_and_names):
                # We check if the current rune is unique by comparing with other runes.
                # We use all function to check current rune is unique by comparing with other runes.
                is_unique = all(
                    current_class[0] != runes_classnames_and_names[j][0]
                    for j in range(len(runes_classnames_and_names))
                    if j != i
                )
                # If it is unique we add name of the rune to the dictionary with the title of the rune.
                # We break the loop to not continue loop our job is done.
                if is_unique:
                    runes[rune_title.text].append(current_class[1])
                    break
        # We print the runes with their titles and names with iterating the dictionary.
        for rune_title, rune_names in runes.items():
            print(f"# {rune_title.upper()} #")
            for rune_name in rune_names:
                print(rune_name)
        # We find the other attributes by using specific classname.
        other_attributes = driver.find_elements(
            By.XPATH, ".//div[contains(@class, 'm-1dj96r2')]"
        )
        # We print the other attributes by iterating the elements.
        # We iterate each other attribute to print them.
        # We find all images of other attributes to get names by reaching alt tag of image.
        print(
            "\n".join(
                "".join(
                    img.get_attribute("alt")
                    for img in other_attribute.find_elements(By.TAG_NAME, "img")
                )
                for other_attribute in other_attributes
            )
        )
        # We find the items by using specific classname.
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'm-1q4a7cx')]")
        print("\n--- BUILD ---")
        # We print the items by iterating the elements.
        # We iterate each item to print names of the items.
        # We find all images of items to get names by reaching alt tag of image.
        print(
            "".join(
                "\n".join(
                    img.get_attribute("alt")
                    for img in item.find_elements(By.TAG_NAME, "img")
                    # We check if the items are under full build title by checking the parent element text.
                    if item.find_element(By.XPATH, "../..")
                    .find_element(By.XPATH, ".//div[contains(@class, 'm-18nhpvr')]")
                    .text
                    == "Full Build"
                )
                for item in items
            )
        )
        print("\n--- ABILITY ORDER ---")
        # We find the abilities by using specific classname.
        abilities = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'm-16bsjni')]"
        )
        # We create a list to store the abilities with their order and key of ability.
        ability_list = []
        # We iterate each ability element to get order and key of the ability.
        for ability in abilities:
            # We find the order of the ability by using specific classname and get text of it.
            ability_order = ability.find_element(
                By.XPATH, ".//div[contains(@class, 'm-1lo8d97')]"
            ).text
            # We find the key of the ability by using specific classname and get text of it.
            ability = ability.find_element(
                By.XPATH, ".//div[contains(@class, 'm-1p6spxi')]"
            ).text
            # We add integer order and key of the ability to the list.
            ability_list.append((int(ability_order), ability))
        # Our ability list is like [[1, 'Q'], [2, 'W'], [3, 'E'], [4, 'Q'], [5, 'Q']]
        # We need to print 4-5 Q instead of 4 Q 5 Q so we need to group ability keys with their orders if they are same consequtively.
        # Current order and key are the first element of the list.
        current_order = ability_list[0][0]
        current_key = ability_list[0][1]
        # We create a string to store the ability order string.
        ability_order_str = f"{current_order}"
        # We iterate each ability to group them by their orders.
        for i in range(1, len(ability_list)):
            # If current key is same with iteration key we add -order to the string.
            if current_key == ability_list[i][1]:
                ability_order_str += f"-{ability_list[i][0]}"
            # If current key is different with iteration key we add space and current key to the string.
            # Then we update current order and key to the iteration order and key.
            # We add new line and current order which is iteration order to the string.
            else:
                ability_order_str += f" {current_key}"
                current_order = ability_list[i][0]
                current_key = ability_list[i][1]
                ability_order_str += f"\n{current_order}"
        # If for loop ends we add last key to the string.
        # Then we check if last key is same with current key if its not we add new line and last abilities order and key to the string.
        # Because if its same we already added it to the string. But we didnt add last ability key to the string.
        # But we add last ability key to the string when loop is over.
        ability_order_str += f" {current_key}"
        if current_key != ability_list[-1][1]:
            ability_order_str += f"\n{ability_list[-1][0]} {ability_list[-1][1]}"
        # We print the ability order string.
        print(ability_order_str)
    except Exception as e:
        print(f"Error occurred: {e}")
    # We need to close browser after fetching data and running our scripts.
    # With while loop we will ask user to enter champion name again and fetch data again.
    driver.quit()
