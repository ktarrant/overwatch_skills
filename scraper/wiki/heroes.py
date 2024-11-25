from bs4 import BeautifulSoup
import requests


wiki_url_root = "https://overwatch.fandom.com/wiki"

# Subcategories in the hero list that are not heroes
ignore_heroes = ["Hero abilities", "Unreleased heroes"]


def get_heroes_list():
    # URL of the Overwatch hero list on the Overwatch wiki
    url = f"{wiki_url_root}/Category:Heroes"

    # Send a request to fetch the HTML content
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find hero information (adjust the selector based on the page's structure)
        heroes = soup.find_all("div", class_="CategoryTreeItem")

        for hero in heroes:
            # Extract the hero name and role
            hero_name = hero.find("a").text.strip()
            hero_link_name = hero_name.replace(" ", "_")
            hero_link = f"{wiki_url_root}/{hero_link_name}"

            if hero_name not in ignore_heroes:
                yield hero_name, hero_link

    else:
        print("Failed to retrieve the page.")


def parse_ability_summary(soup):
    ability = {}

    image_div, summary_div = soup.find_all("div", recursive=False)
    icon_div = image_div.find("div", {"class": "abilityImage"}).find("div", {"class": "center"})
    image_url = icon_div.find("img")["data-src"]
    ability["image_url"] = image_url

    summary_table, summary_text = summary_div.find_all("div", recursive=False)
    for row in summary_table:
        key_name = row.find("b", recursive=False)
        if key_name:
            key_name = key_name.text.strip()
            effect_entries = row.div.find_all("a")
            if effect_entries:
                ability[key_name] = [entry["title"] for entry in effect_entries]
            else:
                ability[key_name] = row.div.text.strip()

        else:
            # This is probably the affected abilities icon row
            affect_icons = row.find_all("div", {"class": "abilityImage"})
            if affect_icons:
                affects = [icon.find("img")["title"] for icon in affect_icons]
                ability["affects"] = affects

    ability["summary"] = summary_text.text.strip()

    return ability


def parse_ability_box(soup):
    ability_sections = soup.find_all("div", recursive=False)
    if len(ability_sections) != 3:
        return None

    ability_header, ability_summary, ability_misc = ability_sections

    # Get the ability name (commonly in an h3 or similar heading tag)
    if "abilityHeader" not in ability_header["class"]:
        return None

    ability_name, ability_control = ability_header.contents

    if "summaryInfoAndImage" not in ability_summary["class"]:
        return None
    ability = parse_ability_summary(ability_summary)

    ability["name"] = ability_name.text.strip()

    ability_control_img = ability_control.find("img")
    if ability_control_img:
        ability["keybind"] = ability_control_img["alt"]

    for misc_row in ability_misc.find_all("div", recursive=False):
        misc_cols = misc_row.find_all("div", recursive=False)
        if len(misc_cols) != 2:
            continue
        key = misc_cols[0].text.strip().rstrip(":")
        value = misc_cols[1].text.strip()
        ability[key] = value

    return ability


def get_hero_abilities(hero_url):
    # Send a request to the hero's page
    response = requests.get(hero_url)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    ability_boxes = soup.find_all("div", {"class": "ability_box"})
    abilities = [parse_ability_box(box) for box in ability_boxes]
    abilities = [ability for ability in abilities if ability]
    return abilities


if __name__ == "__main__":
    import time

    hero_link = f"{wiki_url_root}/Junker_Queen"
    abilities = get_hero_abilities(hero_link)

    if abilities:
        for ability in abilities:
            for key, value in ability.items():
                print(f"{key.title()}: {value}")
            print("-" * 30)

    # for hero_name, hero_link in get_heroes_list():
    #     time.sleep(1)
    #     print(f"Hero Name: {hero_name}")
    #     print(f"Link to Hero Page: {hero_link}")
    #
    #     abilities = get_hero_abilities(hero_link)
    #
    #     if abilities:
    #         for ability in abilities:
    #             print(f"Ability: {ability['name']}")
    #             print(f"Description: {ability['description']}")
    #             print("-" * 30)
    #
    #     print("=" * 30)
    #     break
