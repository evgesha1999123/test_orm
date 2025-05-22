import asyncio
from tortoise import Tortoise
from database import Persons, PersonsFactory
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
         "postgres_models": {
            "models": ["database", "aerich.models"],
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

if __name__ == "__main__":
    async def main():
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        # wr = await get_by_filters()
        # print(wr)
        d = await Persons.all().first()
        print(d)
        is_exist = await Persons.filter(first_name="Иван").exists()
        print(is_exist)
        slovar = await kw()
        print(slovar)
        special_slovar = await kw_special()
        print(special_slovar)
        s = await sorting()
        print(s)
        kv = await get_by_kv()
        print(kv)
        spec = await get_specials_by_kv()
        print(spec)

try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(connections.close_all())
    loop.close()