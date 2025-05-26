from tortoise.models import Model
import tortoise.fields
from tortoise.fields import BackwardFKRelation
from enum import IntEnum
import random
from faker import Faker

first_names = [
    "Иван", "Александр", "Сергей", "Дмитрий", "Андрей",
    "Алексей", "Максим", "Евгений", "Владимир", "Артем",
    "Анна", "Елена", "Ольга", "Наталья", "Мария",
    "Светлана", "Татьяна", "Екатерина", "Ирина", "Юлия"
]

last_names = [
    "Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов",
    "Попов", "Васильев", "Павлов", "Семенов", "Голубев",
    "Виноградова", "Ковалева", "Новикова", "Морозова", "Волкова",
    "Алексеева", "Лебедева", "Соколова", "Козлова", "Егорова"
]

# Связанные таблицы (один ко многим):
# Эта связь подразумевает связь многих записей с одной общей
# В данном кейсе - один турнир имеет много игр
class Game(Model):
    id = tortoise.fields.IntField(pk=True)
    name = tortoise.fields.CharField(max_length=100)
    tournament = tortoise.fields.ForeignKeyField(
        "models.Tournament",
        related_name="games"
    )

class Tournament(Model):
    id = tortoise.fields.IntField(pk=True)
    name = tortoise.fields.CharField(max_length=100)
    games: BackwardFKRelation[Game]


class Persons(Model):
    id = tortoise.fields.IntField(pk=True, generated=True)
    first_name = tortoise.fields.TextField()
    last_name = tortoise.fields.TextField()
    age = tortoise.fields.IntField()
    email = tortoise.fields.TextField()
    phone = tortoise.fields.TextField()
    birth_day_date = tortoise.fields.DateField()

    def __str__(self):
        return f"------------Persons-----------\n{self.first_name}\n{self.last_name}\n{self.age}\n{self.email}\n{self.phone}\n{self.birth_day_date}"


class PersonsFactory:
    async def _generate_randmail():
        str_randmail = ""
        for i in range(12):
            char = chr(random.randint(97, 122))
            capitalization_factor = random.randint(0, 1)
            if capitalization_factor != 0:
                str_randmail += char.capitalize()
            else:
                str_randmail += char
        str_randmail += "@gmail.com" 
        return str_randmail

    @classmethod
    async def generate_person(cls):
        fake = Faker()
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        age = random.randint(18, 100)
        email = await cls._generate_randmail()
        phone = f"+79{random.randint(10**7, 10**8-1)}"
        birth_day_date = fake.date()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "email": email,
            "phone": phone,
            "birth_day_date": birth_day_date
        }


if __name__ == "__main__":
    h = users()
    h._generate_randmail()
    print(h)
