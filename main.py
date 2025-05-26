import asyncio
from tortoise import Tortoise
from models import Persons, PersonsFactory, Tournament, Game
from tortoise import connections
from tortoise.expressions import Q


# Database Configuration for Tortoise ORM
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "maria"
DB_PASSWORD = "maria"
DB_NAME = "maria"

# Tortoise ORM Connection String (async)
TORTOISE_DATABASE_URL = "mysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# Tortoise ORM Configuration
TORTOISE_ORM = {
    "connections": {
        # "default": {
        #     "engine": "tortoise.backends.mysql",
        #     "credentials": {
        #         "host": f"{DB_HOST}",
        #         "port": f"{DB_PORT}",
        #         "user": f"{DB_USER}",
        #         "password": f"{DB_PASSWORD}",
        #         "database": f"{DB_NAME}",
        #     }
        # },
     "default": {  # Второе подключение (PostgreSQL)
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "5432",
                "user": "postgres",
                "password": "postgres",
                "database": "postgres",
            }
        }
    },
    "apps": {
        # "mariadb_models": {
        #     "models": ["database", "aerich.models"],
        #     "default_connection": "default"
        # },
         "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    }
}

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def insert_data():
    human_data = await PersonsFactory.generate_person()
    human = await Persons.create(**human_data)

async def get_data():
    return await Persons.get(id=25)

async def get_q_expr():
    await Persons.get(Q(id=1) | Q(first_name="Павел"))  #OR
    await Persons.get(Q(id=1, first_name="Павел", join_type="OR"))  #Тоже OR, но реализовано в join type
    return await Persons.get(~Q(id=25)) # NOT

async def get_var2():
    user = await Persons.get(id=25)
    user2 = await Persons.get_or_none(id=100) #Не вывалит исключение, если запись с такими параметрами не найдена, вернет None
    user3, was_created = await Persons.get_or_create(id=1) #Если не найдет запись с таким айди, то создаст и вернет в модель, если же запись есть и она одна, то вернет эту запись

async def get_by_filters():
    subscribed_users = await(
        Persons.filter(first_name="Ирина").filter(age=26)
    )
    excluded = await Persons.exclude(age=18, first_name="Иван")
    return subscribed_users

async def kw():
    #Вернет все записи в виде словаря, где ключ это указанные айдишники, а значения - модели из БД
    return await Persons.in_bulk([10,11,12])

async def kw_special():
    return await Persons.in_bulk(["Иван", "Павел"], field_name="first_name")

#Пример сортировки, 1 аргумент - по возрастанию, второй по убыванию
async def sorting():
    return await Persons.all().order_by("age", "-phone")

#Вернет словарь, где ключи-это имена полей, а значения-их содержимое
async def get_by_kv():
    custom_fields = await Persons.first().values("id", "first_name", "last_name", "email")
    return await Persons.first().values()

async def get_listed():
    #В этом случае вернет кортеж с переданными значениями полей
    t = Persons.get(id=200).values_list("email", "phone")
    
    #Вернет список с кортежами состоящий из значений переданного слотбца
    x = Persons.all().values_list("email")

    #В этом случае вернет список всех значений возраста
    a = Persons.all().values_list("age", flat=True)

    #В этом случае вернет кортеж
    return await Persons.get(id=10).values_list()

#Переопределит названия полей на указанные слева от выражений 
async def get_specials_by_kv():
    return await Persons.first().values(
        my_id="id",
        name="first_name",
        test_email="email"
    )

# distinct() - возвращает уникальные элементы из записи
async def get_unique_ages():
    return await Persons.all().distinct().order_by("age").values_list("age", flat=True)

async def modificators():
    users_20_years = await Persons.filter(age=20)
    users_not_20_years = await Persons.filter(age__not=15)
    some_users = await Persons.filter(age__in=(20, 21, 22, 23))
    all_users_except_some = await Persons.filter(age__not_in=(20, 21))
    users_gte = await Persons.filter(age__gte=20)

    grown_users = await Persons.filter(age__range=(20, 30))
    grown_ups = await Persons.filter(age__range(20, 20))
    users_with_email = await Persons.filter(email__isnull=False)
    users_without_email = await Persons.filter(email__not__isnull=False)

    # Поиск подстроки с учетом регистра
    users_with_vi = await Persons.filter(first_name__contains="Ви")
    # Поиск подстроки без учета регистра
    users_with_fe = await Persons.filter(last_name__icontains="фе")
    # Поиск по началу строки
    bro_name = await Persons.filter(first_name__startswith="Па")
    bro_name2 = await Persons.filter(first_name__istartswith="па")

    names_end = await Persons.filter(last_name__endswith="Р")
    names_end2 = await Persons.filter(last_name__iendswith="а")

    # Приводит строку к одному регистру и ищет ее
    evgeniy_user = await Persons.filter(first_name__iexact="ЕвГЕНИЙ").first()
    user_with_nik = await Persons.filter(last_name__search="Ник")

    # Пример поиска по дате с модификатором
    date = await Persons.filter(birth_day_date__year__gte=1970)

async def relation_test():
    tour = await Tournament.create(name="World champ")
    
    game1 = await Game.create(name="Game1", tournament=tour)
    game2 = await Game.create(name="Game2", tournament=tour)
    game3 = await Game.create(name="Game3", tournament=tour)

    return await tour.games.all().filter(name__endswith="2")

if __name__ == "__main__":
    async def main():
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        print(await Game.all().filter(tournament_id=6))

try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(connections.close_all())
    loop.close()