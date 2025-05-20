from tortoise.models import Model
import tortoise.fields
from enum import IntEnum


class User(Model):
    id = tortoise.fields.IntField(primary_key=True)
    age = tortoise.fields.IntField()

    def __str__(self):
        return f"<User : {self.id}\t{self.age}>"

class OrderStatus(IntEnum):
    CANCELLED = 0
    IN_PROCESS = 1
    IN_DELIVERY = 2
    DELIVERED = 3

class users(Model):
    id = tortoise.fields.IntField(pk=True, null=False)
    first_name = tortoise.fields.CharField(max_length=20, null=False)
    last_name = tortoise.fields.CharField(max_length=20, null=False)
    age = tortoise.fields.IntField()
    email = tortoise.fields.CharField(max_length=20, unique=True)
    phone = tortoise.fields.CharField(max_length=20, unique=True)
    birth_day_date = tortoise.fields.CharField(max_length=10, unique=True)


# class Order(Model):
#     id = tortoise.fields.IntField(pk=True)
#     order_status = tortoise.fields.IntEnumFiend