from tests.conftest import client


async def test_create_user_register_success(client: client):
    """Тест успешной регистрации пользователя"""

    response = client.post("/auth/register/", json={
            "username": "test_create_users",
            "email": "test_create_user_register_success@example.com",
            "mobile": "+7 (999) 999-99-99",
            "password": "Passwor123%",
            "password2": "Passwor123%",
    })

    assert response.status_code == 201, response.json()


async def test_create_user_register_existing_email(client: client):
    """Тест регистрации пользователя с существующей почтой"""

    response = client.post("/auth/register/", json={
            "username": "test_existing_email",
            "email": "test_create_user_register_success@example.com",
            "mobile": "+7 (999) 999-99-90",
            "password": "PassworD123%",
            "password2": "PassworD123%",
    })
    assert response.status_code == 400, response.json()
    assert response.json() == {"detail": "такая почта уже существует"}


async def test_create_user_register_existing_mobile(client: client):
    """Тест регистрации пользователя с существующим номером телефона"""

    response = client.post("/auth/register/", json={
            "username": "test_existing_mobile",
            "email": "test_existing_mobiles@example.com",
            "mobile": "+7 (999) 999-99-99",
            "password": "PassworD123%",
            "password2": "PassworD123%",
    })
    assert response.status_code == 400, response.json()
    assert response.json() == {"detail": "такой телефон уже существует"}


async def test_correct_password(client: client):
    """Тест регистрации пользователя на корректность пароля"""

    response = client.post("/auth/register/", json={
            "username": "test_correct_password",
            "email": "test_correct_password@example.com",
            "mobile": "+7 (999) 000-99-99",
            "password": "Passd",
            "password2": "Passd",
    })
    assert response.status_code == 400, response.status_code
    assert response.json() == {'detail': 'Пароль должен быть не менее 8 символов.'}


async def test_correct_password2(client: client):
    """Тест регистрации пользователя на корректность пароля 2"""

    response = client.post("/auth/register/", json={
            "username": "test_correct_password2",
            "email": "test_correct_password2@example.com",
            "mobile": "+7 (999) 001-99-99",
            "password": "PassworD123%",
            "password2": "Passd",
    })
    assert response.status_code == 400, response.status_code
    assert response.json() == {'detail': 'пароли не совпадают'}


async def test_correct_password3(client: client):
    """Тест регистрации пользователя на корректность пароля 3"""

    response = client.post("/auth/register/", json={
            "username": "test_correct_password3",
            "email": "test_correct_password3@example.com",
            "mobile": "+7 (999) 031-99-99",
            "password": "PassworD123",
            "password2": "PassworD123",
    })
    assert response.status_code == 400, response.status_code
    assert response.json() == {'detail': 'Пароль должен содержать хотя бы один спецсимвол из $%&!'}


async def test_correct_password4(client: client):
    """Тест регистрации пользователя на корректность пароля 4"""

    response = client.post("/auth/register/", json={
            "username": "test_correct_password4",
            "email": "test_correct_password4@example.com",
            "mobile": "+7 (990) 031-99-99",
            "password": "password123%",
            "password2": "password123%",
    })
    assert response.status_code == 400, response.status_code
    assert response.json() == {'detail': 'Пароль должен содержать хотя бы один символ верхнего регистра.'}


async def test_uncorrect_email(client: client):
    """Тест регистрации пользователя с неверной почтой"""

    response = client.post("/auth/register/", json={
            "username": "test_uncorrect_email",
            "email": "test_uncorrect_email.com",
            "mobile": "+7 (920) 031-99-99",
            "password": "passworD123%",
            "password2": "passworD123%",
    })
    assert response.status_code == 422, response.status_code


async def test_uncorrect_mobile(client: client):
    """Тест регистрации пользователя с неверным телефоном"""

    response = client.post("/auth/register/", json={
            "username": "test_uncorrect_mobile",
            "email": "test_uncorrect_mobile@dfdsf.com",
            "mobile": "+7 (920 031-99-99",
            "password": "passworD123%",
            "password2": "passworD123%",
    })
    assert response.status_code == 400, response.text
    assert response.json()['detail'] == 'Неверный формат телефонного номера.'
