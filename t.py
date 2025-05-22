import random

str_randmail = ""

for i in range(12):
    char = chr(random.randint(97, 122))
    capitalization_factor = random.randint(0, 1)
    if capitalization_factor != 0:
        str_randmail += char.capitalize()
    else:
        str_randmail += char

str_randmail = f"{str_randmail}@gmail.com"
print(str_randmail)