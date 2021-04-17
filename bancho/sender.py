from bancho.writer import Writer
from config import config
import aiohttp

async def send(data: Writer) -> None:
    headers = {
        "User-Agent": "osu!",
        "akari-cikey": config["akari-cikey"]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://c.ainu.pw/", data=data, headers=headers) as r:
            print("%s, has been sent" % (data))
