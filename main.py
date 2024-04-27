from telegram import Bot
from telegram.ext import Application

import requests
from bs4 import BeautifulSoup

import asyncio
from datetime import datetime

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


async def send_message(bot):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=get_message())
        print(f"{datetime.now()} : Message sent")
    except Exception as e:
        print(f"Failed to send message: {e}")


async def periodic_message():
    bot = Bot(TG_TOKEN)
    while True:
        await send_message(bot)
        await asyncio.sleep(300)  # sleep for 300 seconds


def main():
    """Create the bot and run the periodic messaging task."""
    _ = Application.builder().token(TG_TOKEN).build()

    asyncio.run(periodic_message())


if __name__ == '__main__':
    main()
