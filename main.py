import time
from rpgitems.scraper import RpgItems

with RpgItems(teardown=False) as bot:
    bot.get_first_page()
    bot.get_rpg_items_in_the_page()
    links = bot.get_rpg_items_in_the_page()
    bot.get_rpg_item_data(links)
    time.sleep(1)
