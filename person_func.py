from aiohttp import ClientSession
from models import Session, Person

async def insert_people(person: dict):  # функция записи персонажей в БД
    async with Session() as session:
                if person:
                    session.add(Person(**person)) # здесь почему то если использовать add_all то пытается записать None объект
                    try:
                        await session.commit()
                        print(f"Персонаж {person.get('name')} Записан в БД")
                    except Exception as e:
                        print("Персонаж уже сущетвует")
                        # print(e)

async def get_people(people_id: int, client: ClientSession):  # получаем список с json-ами
    response = await client.get(f"https://swapi.dev/api/people/{people_id}")
    if response.status == 200:
        response_json = await response.json()
        return response_json


# функции для получения названий из ссылок
async def get_planets(link: str, client: ClientSession):
    response = await client.get(link)
    response_json = await response.json()
    return response_json

async def get_films(link: str, client: ClientSession):
    response = await client.get(link)
    response_json = await response.json()
    return response_json
async def get_starships(link: str, client: ClientSession):
    response = await client.get(link)
    response_json = await response.json()
    return response_json
async def get_vehicles(link: str, client: ClientSession):
    response = await client.get(link)
    response_json = await response.json()
    return response_json
async def get_species(link: str, client: ClientSession):
    response = await client.get(link)
    response_json = await response.json()
    return response_json



async def clean_persons(list_of_persons: list[dict], client: ClientSession):
    for person in list_of_persons:
        if person is not None:
            person['id'] = int(person.pop('url').split("/")[-2])  # добавляем айди в виде цифры

            #  заменяем ссылки на слова
            if len(person['homeworld']) > 0:
                response = await get_planets(person['homeworld'], client)
                person['homeworld'] = response.get('name')
            else:
                person['homeworld'] = "n/a"

            if len(person['films']) > 0:
                films = []
                for film in person['films']:
                    response = await get_films(film, client)
                    films.append(response.get('title'))
                person['films'] = ", ".join(films)
            else:
                person['films'] = "n/a"

            if len(person['starships']) > 0:
                starships = []
                for starship in person['starships']:
                    response = await get_starships(starship, client)
                    starships.append(response.get('name'))
                person['starships'] = ", ".join(starships)
            else:
                person['starships'] = "n/a"

            if len(person['vehicles']) > 0:
                vehicles = []
                for vehicle in person['vehicles']:
                    response = await get_vehicles(vehicle, client)
                    vehicles.append(response.get('name'))
                person['vehicles'] = ", ".join(vehicles)
            else:
                person['vehicles'] = "n/a"

            if len(person['species']) > 0:
                species = []
                for specie in person['species']:
                    response = await get_species(specie, client)
                    species.append(response.get('name'))
                person['species'] = ", ".join(species)
            else:
                person['species'] = "n/a"

            person.pop('created') # удаляем лишние ключи
            person.pop('edited')

            print(f"Персонаж {person.get('name')} готов")
            await insert_people(person)
