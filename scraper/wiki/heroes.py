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


def get_hero_abilities(hero_url):
    # Send a request to the hero's page
    response = requests.get(hero_url)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the Abilities section - typically an HTML element with a specific header or class
    abilities_section = soup.find("span", {"id": "Abilities"})
    if not abilities_section:
        print("Abilities section not found.")
        return None

    # Move to the parent element to access the list of abilities
    abilities_cur = abilities_section.find_parent("h2").find_next_sibling("div")

    # Extract each ability and description
    abilities = []
    while abilities_cur.name != "h2":
        if abilities_cur.name == "div":
            # Get the ability name (commonly in an h3 or similar heading tag)
            ability_header = abilities_cur.find("div", {"class": "abilityHeader"})
            if not ability_header:
                continue

            ability_name, ability_control = ability_header.contents

            ability_control_img = ability_control.find("img")
            if ability_control_img:
                control = ability_control_img["alt"]
            else:
                control = ability_control.text.strip()

            # Add the ability to the list
            abilities.append({
                "name": ability_name.text.strip(),
                "control": control
            })

        abilities_cur = abilities_cur.next_sibling

    return abilities


if __name__ == "__main__":
    import time

    hero_link = f"{wiki_url_root}/Junker_Queen"
    abilities = get_hero_abilities(hero_link)

    if abilities:
        for ability in abilities:
            print(f"Ability: {ability['name']}")
            print(f"Control: {ability['control']}")
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
