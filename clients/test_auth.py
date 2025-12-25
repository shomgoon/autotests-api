from AuthenticationClient import get_authentication_client


def test_login_correct():
    """Тестируем логин с правильной обработкой ответа."""

    print("=" * 60)
    print("ТЕСТ АВТОРИЗАЦИИ (исправленная версия)")
    print("=" * 60)

    # 1. СОЗДАЁМ КЛИЕНТ
    auth_client = get_authentication_client()
    print(f"✅ Клиент создан: {type(auth_client).__name__}")

    # 2. ПОДГОТАВЛИВАЕМ ДАННЫЕ (используем рабочие credentials!)
    login_data = {
        "email": "test_1766651144.071143@email.com",
        "password": "string"
    }

    print(f"\n📤 Отправляем запрос на логин...")

    try:
        # 3. ВЫЗЫВАЕМ МЕТОД LOGIN
        response = auth_client.login_api(login_data)

        print(f"\n📥 Ответ сервера:")
        print(f"   Статус: {response.status_code}")

        # 4. ОБРАБАТЫВАЕМ ОТВЕТ
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ УСПЕШНЫЙ ЛОГИН!")

            # Ищем токен в структуре ответа
            if "token" in data and "accessToken" in data["token"]:
                access_token = data["token"]["accessToken"]
                refresh_token = data["token"]["refreshToken"]
                token_type = data["token"]["tokenType"]

                print(f"   Тип токена: {token_type}")
                print(f"   Access Token: {access_token[:50]}...")
                print(f"   Refresh Token: {refresh_token[:50]}...")

                # Сохраняем токены для дальнейшего использования
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": token_type
                }
            else:
                print("   ⚠️ Неожиданная структура ответа:")
                print(f"   {data}")
                return None

        else:
            print(f"\n❌ ОШИБКА: {response.status_code}")
            print(f"   Тело ответа: {response.text}")

    except Exception as e:
        print(f"\n❌ ОШИБКА ВЫПОЛНЕНИЯ:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    return None


def test_refresh_token():
    """Тестируем обновление токена."""

    # Сначала получаем токен через логин
    tokens = test_login_correct()

    if not tokens:
        print("❌ Не удалось получить токен для теста refresh")
        return

    print("\n" + "=" * 60)
    print("ТЕСТ ОБНОВЛЕНИЯ ТОКЕНА (refresh)")
    print("=" * 60)

    auth_client = get_authentication_client()

    refresh_data = {
        "refreshToken": tokens["refresh_token"]
    }

    print(f"📤 Отправляем refresh token...")

    try:
        response = auth_client.refresh_api(refresh_data)

        print(f"\n📥 Ответ сервера:")
        print(f"   Статус: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Токен обновлён!")

            # Новая структура токена
            if "token" in data and "accessToken" in data["token"]:
                new_access_token = data["token"]["accessToken"]
                new_refresh_token = data["token"]["refreshToken"]

                print(f"   Новый Access Token: {new_access_token[:50]}...")
                print(f"   Новый Refresh Token: {new_refresh_token[:50]}...")

                return {
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token
                }
        else:
            print(f"❌ Ошибка обновления: {response.status_code}")
            print(f"   Тело: {response.text}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


def test_authorized_request():
    """Тестируем запрос с токеном авторизации."""

    # Получаем токен
    tokens = test_login_correct()

    if not tokens:
        return

    print("\n" + "=" * 60)
    print("ТЕСТ ЗАПРОСА С ТОКЕНОМ")
    print("=" * 60)

    # Для авторизованных запросов нужен клиент с токеном
    # Пока делаем вручную (в следующем уроке будет Private Builder)

    import httpx

    # Создаём клиент с токеном
    authorized_client = httpx.Client(
        base_url="http://localhost:8000",
        headers={
            "Authorization": f"{tokens['token_type']} {tokens['access_token']}",
            "Content-Type": "application/json"
        },
        timeout=30
    )

    # Пробуем защищённый endpoint
    endpoints_to_test = [
        "/api/v1/users/me",           # Информация о текущем пользователе
        "/api/v1/courses",            # Список курсов
        "/api/v1/exercises",          # Упражнения
    ]

    for endpoint in endpoints_to_test:
        print(f"\n🔍 Тестируем {endpoint}:")

        try:
            response = authorized_client.get(endpoint)
            print(f"   Статус: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Успех! Данные получены")
                # Можно вывести краткую информацию
                if endpoint == "/api/v1/users/me":
                    print(f"   Пользователь: {data.get('user', {}).get('email', 'N/A')}")
                elif endpoint == "/api/v1/courses":
                    print(f"   Количество курсов: {len(data) if isinstance(data, list) else 'N/A'}")
            elif response.status_code == 401:
                print(f"   ❌ Не авторизован (токен не принят)")
            elif response.status_code == 403:
                print(f"   ⚠️ Доступ запрещён (нет прав)")
            else:
                print(f"   ⚠️ Неожиданный статус")

        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


if __name__ == "__main__":
    print("🚀 ЗАПУСК ТЕСТОВ АВТОРИЗАЦИИ")
    print("=" * 60)

    # Тест 1: Логин
    tokens = test_login_correct()

    if tokens:
        # Тест 2: Refresh token
        test_refresh_token()

        # Тест 3: Авторизованные запросы
        test_authorized_request()

    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("=" * 60)