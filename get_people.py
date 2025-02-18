import asyncio
from aiohttp import ClientSession
from more_itertools import chunked
import requests as r
from person_func import get_people, clean_persons
from models import int_orm, close_orm

MAX_REQUESTS_SIZE = 5
MAX_PEOPLE_COUNT = r.get("https://swapi.dev/api/people/").json().get("count")  # получаем общее количество персонажей

async def main():
    await int_orm()
    row_people = []  # список со списками персонажей
    async with ClientSession() as client:
        for people_ids in chunked(range(1, MAX_PEOPLE_COUNT+1), MAX_REQUESTS_SIZE):  # делим запросы по 5 штук и отправляем
            response = (get_people(i, client) for i in people_ids)
            row_people.append(await asyncio.gather(*response))

        for person_list in row_people:  # "очищаем" словари персонажей
            await clean_persons(person_list, client)

        await close_orm()

asyncio.run(main())