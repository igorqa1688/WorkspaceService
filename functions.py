import grpc
import uuid
import random
import string
from global_vars import server


# Генерация GUID
def generate_guid() -> str:
    return str(uuid.uuid4())


# Создание gRPC-канала для подключения к серверу
def grpc_channel():
    with grpc.insecure_channel(server) as channel:
        yield channel


# Генерация случайной строки
def generate_random_string(length: int) -> str:
    # Определяем необходимые наборы символов
    lower_chars = 'abcdefghijklmnopqrstuvwxyz'
    upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyrillic_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    digits = '0123456789'
    special_chars = '!@#$%^&*()_+~`|}{[]:;?><,./-='

    # Добавляем как минимум один символ каждого типа
    result = random.choice(digits) + \
             random.choice(special_chars) + \
             random.choice(lower_chars) + \
             random.choice(upper_chars) + \
             random.choice(cyrillic_chars)

    # Заполняем оставшуюся часть случайными символами
    remaining_length = length - len(result)
    result += ''.join(random.choices(lower_chars + upper_chars + digits + special_chars + cyrillic_chars, k=remaining_length))
    random_string = ''.join(random.sample(result, len(result)))
    # Перемешиваем символы
    return random_string


# Генерация случайного описания workspace
def generate_workspace_description(length: int) -> str:
    # Создаем списки разных типов символов
    lower_chars = 'abcdefghijklmnopqrstuvwxyz'
    upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyrillic_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    digits = '0123456789'
    special_chars = '!@#$%^&*()_+~`|}{[]:;?><,./-='

    # Создаем список всех доступных символов
    all_chars = lower_chars + upper_chars + digits + special_chars + cyrillic_chars

    # Создаем начальные части строки
    result = random.choice(digits)
    result += random.choice(special_chars)
    result += random.choice(lower_chars)
    result += random.choice(upper_chars)
    result += random.choice(cyrillic_chars)

    # Заполняем оставшуюся часть случайными символами
    while len(result) < length:
        result += random.choice(all_chars)

    # Перемешиваем символы
    return ''.join(random.sample(result, len(result)))


def random_role(roles: list) -> str:
    random_index = random.randint(0, len(roles) - 1)

    if random_index == len(user_roles):
        random_role = "ROLE INDEX EQUAL ARRAY LENGTH"
        return random_role
    else:
        random_role = roles[random_index]
        return random_role