import bs4 as bs
from selenium import webdriver
import os
import time


class Scrapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_top_clans() -> dict:
        # WG page is dynamic, and a pain to scrap.... download table because I am lazy...
        file = os.path.join(os.getcwd(), "wotleadertable.html")
        with open(file, 'r') as fp:
            html = fp.read()
        # Soup time
        wot_soup = bs.BeautifulSoup(html, features="html.parser")

        # Get each row of the tale
        clans = wot_soup.find_all("span", class_='clan-name leaderboards__clan js-tooltip')

        # Store the pair: [ClanTag] : ClanID
        clan_dict = {}

        # Iterate over each clan, get the name and the id, insert into the dictionary
        for clan in clans:
            clan_id = clan.attrs['data-clan-id']
            clan_name = clan.find("span", class_='clan-name_tag').text
            clan_dict[clan_name] = clan_id

        return clan_dict

    @staticmethod
    def get_clan_tools_data(clan_id) -> str:
        # Format the URL
        base_url = "https://clantools.us/servers/na/fame?clan_id={}&e=metal_wars&f=metal_wars_bg".format(clan_id)

        # The find we are getting
        battles = ""
        win_rate = ""
        tank_want = ""
        tank_got = ""

        # Dynamically loading page. Wait for it to populate
        path = os.getcwd()  # CHANGE TO WHERE YOUR GECKODRIVER IS# CHANGE TO WHERE YOUR GECKODRIVER IS
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(path, options=options)

        browser.get(base_url)

        # Sleep 15 seconds, about the loading time for me. Change to be faster/slower as needed
        time.sleep(15)

        # Extract the html
        html = browser.page_source
        clan_tool_soup = bs.BeautifulSoup(html, features="html.parser")
        tank_want = clan_tool_soup.find(id='clan_lic_eligible_members').text
        tank_got = clan_tool_soup.find(id='clan_tanks_for_members').text
        battles = clan_tool_soup.find(id='clan_battles').text
        win_rate = clan_tool_soup.find(id='clan_win_rate').text

        return Scrapper.format_string(tank_want, tank_got, battles, win_rate)

    @staticmethod
    def format_string(tank_want, tank_got, battles, win_rate) -> str:
        return "{},{},{},{}".format(tank_want, tank_got, battles, win_rate)