from telegram import Bot

import requests
from bs4 import BeautifulSoup

from pyowm import OWM
from pyowm.utils.config import get_default_config

import asyncio
import schedule
import time

TG_TOKEN = open("tg_api_token.txt").read()
CHANNEL_ID = '@GoKupatsya'

URL_WATER = "http://worldseatemp.com/ru/Cyprus/Limassol/"

WEATHER_URL = "https://weather.com/ru-RU/weather/hourbyhour/l/Limassol+Limassol+Cyprus?canonicalCityId=a2db05887febdeeef946bcca01cee4e710f05b137599c22e5551217d1156430b"


class SelectorNotFoundException(Exception):
    """Exception raised when no elements match the given CSS selector."""

    def __init__(self, selector, message="No elements found matching the selector"):
        self.selector = selector
        self.message = message
        super().__init__(f"{message}: {selector}")


def watter_temp():
    try:
        response = requests.get(URL_WATER)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        water_temp = soup.select_one("#current > div > table").findAll("td")[1].text
        if not water_temp:
            raise SelectorNotFoundException
        return water_temp

    except requests.RequestException as e:
        print(f"Error during requests to {URL_WATER}: {str(e)}")
        return "🤷‍"


def temp_uv():
    try:
        response = requests.get(WEATHER_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        air_temp = soup.select_one(
            "#detailIndex0 > summary > div > div > div.DetailsSummary--temperature--1kVVp > span").text
        uv_index = soup.select_one("#detailIndex0 > div > div.DaypartDetails--DetailsTable--1zK4r.DetailsTable"
                                   "--flexColumn--2fOHz > ul > li:nth-child(4) > div > "
                                   "span.DetailsTable--value--2YD0-").text
        if not air_temp or not uv_index:
            raise SelectorNotFoundException
        return air_temp, uv_index

    except requests.RequestException as e:
        print(f"Error during requests to {URL_WATER}: {str(e)}")
        return "🤷‍"


def get_message():
    wt = watter_temp()
    at, uv = temp_uv()
    return f"🌊: {wt}, 💨: {at}, ☀️: {uv}"


async def main():
    bot = Bot(TG_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=get_message())

    # schedule.every().hour.do(hourly_message, bot=bot)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)  # Sleep for 1 second between checks


if __name__ == '__main__':
    print(get_message())
