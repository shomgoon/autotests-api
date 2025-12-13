import httpx
from tools.fakers import get_random_email, get_random_data  # Импортируем функцим для генерации случайных данных

# создание пользователя

create_user_payload = {
    "email": get_random_email(),  # Используем функцию для генерации случайного email
    "password": get_random_data()["pass"],
    "lastName": get_random_data()["last_name"],
    "firstName": get_random_data()["first_name"],
    "middleName": get_random_data()["middle_name"]
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print(f'Статус код ответа {create_user_response.status_code}')
print(create_user_response_data)

print('Проходим аутентификацию...')
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

print('Обновляем данные пользователя...')
patch_user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}
patch_user_payload = {
    #"email": get_random_email(),  # Используем функцию для генерации случайного email
    #"password": get_random_data()["pass"],
    "lastName": get_random_data()["last_name"],
    "firstName": get_random_data()["first_name"],
    "middleName": get_random_data()["middle_name"]
}

patch_user_response = httpx.patch(
    f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}",
    json=patch_user_payload,
    headers=patch_user_headers
)
patch_user_response_data = patch_user_response.json()
print('Get user data:', patch_user_response_data)
