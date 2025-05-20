import asyncio
from tortoise import Tortoise
from database import User, users
from tortoise import connections


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
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": f"{DB_HOST}",
                "port": f"{DB_PORT}",
                "user": f"{DB_USER}",
                "password": f"{DB_PASSWORD}",
                "database": f"{DB_NAME}",
            }
        },
     "postgres": {  # Второе подключение (PostgreSQL)
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
        "mariadb_models": {
            "models": ["database", "aerich.models"],
            "default_connection": "default"
        },
         "postgres_models": {
            "models": ["database", "aerich.models"],
            "default_connection": "postgres"
        }
    }
}

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def test_maria():
    maria_conn = connections.get("default")

    user = await User.create(age=18)
    print(user)

    new_user = User(age=25)
    await new_user.save()

async def test_post():
    postgres_conn = connections.get("postgres")

    human = await users(
        id = 0,
        first_name="Abeme",
        last_name="Obeme",
        age=54,
        email="abema123@gmail.com",
        phone="+79781488228",
        birth_day_date="11.02.1377",
    ).save(using_db=postgres_conn)

    print(human)

if __name__ == "__main__":
    async def main():
        
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

        await test_maria()
        await test_post()

try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(connections.close_all())
    loop.close()