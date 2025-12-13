import httpx

response = httpx.get('https://jsonplaceholder.typicode.com/todos/201')
print(response.status_code)
print(response.json())
print(response)
print('Запрос на 201')


data = {
    'title': 'GP',
    'completed': False,
    'userID': 1
}
response = httpx.post('https://jsonplaceholder.typicode.com/todos', json=data)
print(response.status_code)
print(response.headers)
print(response.json)
print('Пост GP')

#data = {"username": "test_user", "password": "123456"}

#response = httpx.post("https://httpbin.org/post", data=data)
#print(response.status_code)
#print(response.headers)
#print('Пост data')


###headers = {"Authorization": "Bearer my_secret_token"}

#response = httpx.get("https://httpbin.org/get", headers=headers)

#print(response.json)  # Заголовки включены в ответ
#print('Запрос заголовки')
params = {'userID': 1}
response = httpx.get('https://jsonplaceholder.typicode.com/todos', params=params)
print(response.url)
print(response.json())