from telegram import Bot
import asyncio
import requests
from bs4 import BeautifulSoup
import schedule
import time

TG_TOKEN = open("tg_api_token.txt").read()
CHANNEL_ID = '@GoKupatsya'

URL_WATER = "http://worldseatemp.com/ru/Cyprus/Limassol/"



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
        temp = soup.select_one("#current > div > table").findAll("td")[1].text
        if not temp:
            raise SelectorNotFoundException
        return temp

    except requests.RequestException as e:
        print(f"Error during requests to {URL_WATER}: {str(e)}")
        return "🤷‍"

def temp_uv():
    querystring = {
        "location": "34.688440, 33.068460",
        "fields": ["temperature", "uvIndex"],
        "units": "metric",
        "timesteps": "current",
        "apikey": "your-api-key"
    }

    response = requests.request("GET", url, params=querystring)
    data = response.json()
    current_weather = data['data']['timelines'][0]['intervals'][0]['values']

    temperature = current_weather['temperature']
    uv_index = current_weather['uvIndex']


def get_message():
    return f"🌊: {watter_temp()}, 💨: 31, ☀️: 6.0"


async def main():
    bot = Bot(TG_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=get_message())

    # schedule.every().hour.do(hourly_message, bot=bot)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)  # Sleep for 1 second between checks


if __name__ == '__main__':
    print(watter_temp())
