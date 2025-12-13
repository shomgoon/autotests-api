import time
import random
import string

def get_random_email() -> str:
    return f'test_{time.time()}@email.com'


# 1. Генерация случайных данных
def get_random_data() -> str:
    return {
        "first_name": f"User{random.randint(1, 1000)}",
        "last_name": f"Test{random.randint(1, 1000)}",
        "middle_name": f"Test{random.randint(1, 1000)}",
        #"pass": f"pass{random.randint(10, 1000)}"  # Уникальный pass
        "pass": ''.join(random.choices(string.digits, k=6)) # Уникальный pass
        }
