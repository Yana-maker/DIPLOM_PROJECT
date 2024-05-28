# TA4 дипломный проект
# **./main.py**

Этот проект демонстрирует приложение FastAPI с маршрутами для аутентификации пользователей, 
функциональными возможностями пользователей, продуктов и корзины.

### Настройка


1. установите необходимые переменные в setting.py
2. Установите необходимые зависимости, запустив pip install -r requirements.txt.
3. Настройте базу данных, создав папку базы данных с помощью models.py для определения моделей базы данных и db.py для установления подключения к базе данных.
4. Настройте подключение к базе данных в файле database.db.
5. Запустите приложение FastAPI, выполнив команду uvicorn main:app --reload.

### Структура проекта

- main.py: Содержит приложение FastAPI и включает маршруты для аутентификации пользователей, продуктов и корзины.
- database/models.py: Определяет модели SQLAlchemy для таблиц базы данных.
- database/db.py: Устанавливает подключение к базе данных с помощью SQLAlchemy.
- routes/auth.py: Обрабатывает маршруты аутентификации.
- routes/users.py: Обрабатывает маршруты, связанные с пользователем.
- routes/products.py: Обрабатывает маршруты, связанные с продуктами.
- routes/cart.py: Обрабатывает маршруты, связанные с корзиной.
- utils/auth.py: содержит дополнительные функции для обработки маршрутов аутентификации
- utils/support_functions.py: содержит дополнительные функции проверки и хеширования пароля

 



# **папка routes**

1.1 **routes/auth.py**
Этот файл содержит описание кода, отвечающего за аутентификацию пользователей в приложении.

### Описание
регистрация, вход и получение информации о текущем пользователе. 
код использует FastAPI для создания API, 
SQLAlchemy для работы с базой данных, 
bcrypt для хеширования паролей и JWT для генерации токенов.

### Функции

#### `create_user_register`

Функция, отвечающая за регистрацию нового пользователя.

- Аргументы:
    - `db`: Объект подключения к базе данных.
    - `create_user_request`: Данные для создания нового пользователя.
- Действия:
    - Проверяет, существует ли уже пользователь с указанным email или номером телефона.
    - Хеширует пароль и сохраняет данные пользователя в базу данных.
    - Возвращает данные пользователя, которые были созданы.

#### `login_for_access_token`

Функция, отвечающая за создание JWT-токена для авторизации пользователя.

- Аргументы:
    - `form_data`: Данные авторизации пользователя (login, password).
    - `db`: Объект подключения к базе данных.
- Действия:
    - Аутентифицирует пользователя, проверяя правильность login и password.
    - Генерирует JWT-токен и возвращает его.

#### `login_user`

Функция, отвечающая за вход в систему по email или номеру телефона.

- Аргументы:
    - `db`: Объект подключения к базе данных.
    - `form_data`: Данные для входа (login, password).
- Действия:
    - Находит пользователя по email или номеру телефона.
    - Проверяет правильность пароля.
    - Генерирует JWT-токен и возвращает его.

#### `user`
Функция, отвечающая за получение информации о текущем авторизированном пользователе.

- Аргументы:
    - `user_db`: Данные о текущем авторизированном пользователе (получаются через декоратор `Depends(user_dependency)`).
    - `db`: Объект подключения к базе данных.
- Действия:
    - Проверяет, авторизован ли пользователь.
    - Возвращает информацию о пользователе.

### Использование

- Для регистрации нового пользователя отправьте POST-запрос на `/auth/register` с данными пользователя в теле запроса.
- Для получения JWT-токена отправьте POST-запрос на `/auth/token` с данными для авторизации (login, password) в теле запроса.
- Для входа в систему по email или номеру телефона отправьте POST-запрос на `/auth/login` с данными для входа (login, password) в теле запроса.
- Для получения информации о текущем авторизированном пользователе отправьте GET-запрос на `/auth/me`.

### Дополнительная информация

- Декоратор `Depends(user_dependency)` используется для проверки авторизации пользователя.
- Функция `get_by_email_or_mobile_user` используется для поиска пользователя по email или номеру телефона.
- Функция `create_access_token` используется для генерации JWT-токена.
- Функция `authenticate_user` используется для аутентификации пользователя.

### Заметки

- Код содержит базовую реализацию аутентификации пользователей. 
- В реальном приложении может потребоваться добавить дополнительные функции, такие как:
    - Отправка email-уведомлений при регистрации.
    - Включение двухфакторной аутентификации.
    - Реализация различных ролей пользователей.

1.2 **routes/cart.py**

Этот файл содержит описание кода, отвечающего за обработку корзины в приложении.

### Описание
Код реализует создание, чтение и удаления корзин. 
Он использует FastAPI для создания API, 
SQLAlchemy для работы с базой данных, 
а также JWT для авторизации пользователей.

### Функции

#### `create_cart`

Функция, отвечающая за создание новой корзины.

- Аргументы:
    - `cart`: Данные корзины, которые нужно добавить.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Добавляет каждый продукт из корзины в базу данных.
    - Возвращает данные добавленной корзины.

#### `read_cart`

Функция, отвечающая за чтение информации о корзине.

- Аргументы:
    - `cart_id`: ID корзины, которую нужно прочитать.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит корзину по ID.
    - Возвращает сумму цен всех продуктов в корзине.

#### `delete_cart`

Функция, отвечающая за удаление корзины.

- Аргументы:
    - `cart_id`: ID корзины, которую нужно удалить.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит корзину по ID.
    - Удаляет корзину из базы данных.
    - Возвращает данные удаленной корзины.

### Использование

- Для создания новой корзины отправьте POST-запрос на `/cart/create` с данными корзины в теле запроса.
- Для чтения информации о корзине отправьте GET-запрос на `/cart/read/{cart_id}`.
- Для удаления корзины отправьте DELETE-запрос на `/cart/delete/{cart_id}`.

### Дополнительная информация

- Декоратор `Depends(get_current_user)` используется для проверки авторизации пользователя.
- Функция `get_current_user` используется для получения данных о текущем авторизованном пользователе.

1.3 **routes/products.py**

Этот файл содержит описание кода, отвечающего за обработку продуктов в приложении.

### Описание
Код реализует создание, чтения, удаления и обновления продуктов. 
Он использует FastAPI для создания API, 
SQLAlchemy для работы с базой данных, 
а также JWT для авторизации пользователей.

### Функции

#### `create_product`

Функция, отвечающая за создание нового продукта.

- Аргументы:
    - `product`: Данные продукта, которые нужно добавить.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Создает новый объект продукта в базе данных.
    - Возвращает данные добавленного продукта.

#### `read_product`

Функция, отвечающая за чтение информации о продукте.

- Аргументы:
    - `product_id`: ID продукта, который нужно прочитать.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит продукт по ID.
    - Возвращает данные продукта.

#### `delete_product`

Функция, отвечающая за удаление продукта.

- Аргументы:
    - `product_id`: ID продукта, который нужно удалить.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит продукт по ID.
    - Удаляет продукт из базы данных.
    - Возвращает данные удаленного продукта.

#### `update_product`

Функция, отвечающая за обновление данных продукта.

- Аргументы:
    - `product_id`: ID продукта, который нужно обновить.
    - `product`: Новые данные продукта.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит продукт по ID.
    - Обновляет данные продукта в базе данных.
    - Возвращает данные обновленного продукта.

### Использование

- Для создания нового продукта отправьте POST-запрос на `/products/create` с данными продукта в теле запроса.
- Для чтения информации о продукте отправьте GET-запрос на `/products/read/{product_id}`.
- Для удаления продукта отправьте DELETE-запрос на `/products/delete/{product_id}`.
- Для обновления данных продукта отправьте PUT-запрос на `/products/update/{product_id}` с новыми данными продукта в теле запроса.

### Дополнительная информация

- Декоратор `Depends(get_current_user)` используется для проверки авторизации пользователя.
- Функция `get_current_user` используется для получения данных о текущем авторизованном пользователе.



1.4 **routes/users.py**

Этот файл содержит описание кода, отвечающего за обработку пользователей в приложении.

### Описание

Код реализует создание, чтения, удаления и обновления пользователей. 
Он использует FastAPI для создания API, 
SQLAlchemy для работы с базой данных, 
bcrypt для хеширования паролей, 
а также JWT для авторизации пользователей.

### Функции

#### `create_user`

Функция, отвечающая за создание нового пользователя.

- Аргументы:
    - `user`: Данные пользователя, которые нужно добавить.
    - `db`: Объект подключения к базе данных.
- Действия:
    - Хеширует пароль пользователя с помощью bcrypt.
    - Создает нового пользователя в базе данных.
    - Возвращает данные созданного пользователя.

#### `read_user`

Функция, отвечающая за чтение информации о пользователе.

- Аргументы:
    - `user_id`: ID пользователя, который нужно прочитать.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит пользователя по ID.
    - Возвращает данные пользователя.

#### `delete_user`

Функция, отвечающая за удаление пользователя.

- Аргументы:
    - `user_id`: ID пользователя, который нужно удалить.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит пользователя по ID.
    - Удаляет пользователя из базы данных.
    - Возвращает данные удаленного пользователя.

#### `update_user`

Функция, отвечающая за обновление данных пользователя.

- Аргументы:
    - `user_id`: ID пользователя, который нужно обновить.
    - `user`: Новые данные пользователя.
    - `db`: Объект подключения к базе данных.
    - `current_user`: Текущий авторизованный пользователь (получается через декоратор `Depends(get_current_user)`).
- Действия:
    - Находит пользователя по ID.
    - Обновляет данные пользователя в базе данных.
    - Возвращает данные обновленного пользователя.

### Использование

- Для создания нового пользователя отправьте POST-запрос на `/users/create` с данными пользователя в теле запроса.
- Для чтения информации о пользователе отправьте GET-запрос на `/users/read/{user_id}`.
- Для удаления пользователя отправьте DELETE-запрос на `/users/delete/{user_id}`.
- Для обновления данных пользователя отправьте PUT-запрос на `/users/put/{user_id}` с новыми данными пользователя в теле запроса.

### Дополнительная информация

- Декоратор `Depends(get_current_user)` используется для проверки авторизации пользователя.
- Функция `get_current_user` используется для получения данных о текущем авторизованном пользователе.



# **папка database**

1.1 **database/schemas.py**

Этот файл содержит описание модели пользователя и модели продукта, которые используются в приложении.

### Модели:

#### Модель пользователя
class User(BaseModel):
    """Модель пользователя"""

    is_active: Optional[bool] = True
    username: str
    email: EmailStr
    mobile: str
    password: str
    password2: str

Модель пользователя содержит следующие поля:

- `is_active`: Флаг, указывающий на активность пользователя (по умолчанию `True`).
- `username`: Имя пользователя.
- `email`: Электронный адрес.
- `mobile`: Мобильный телефон.
- `password`: Пароль.
- `password2`: Повторение пароля.

#### Модель входа
class LoginUser(BaseModel):
    login: str
    password: str

Модель для входа в систему содержит:

- `login`: Логин пользователя (может быть `username` или `email`).
- `password`: Пароль.

#### Модель создания пользователя
class CreateUserRequest(User):

    username: str
    email: EmailStr
    mobile: str
    password: str
    password2: str

    # Валидация полей
    ...

Модель для создания пользователя наследует поля модели `User` и добавляет валидацию для следующих полей:

- `mobile`: Валидация телефонного номера.
- `password`: Валидация пароля (длина, наличие символов).
- `password2`: Проверка совпадения паролей.

#### Модель продукта
class Product(BaseModel):
    """Модель продукта"""
    title: str
    description: Optional[str] = None
    price: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: bool
    owner: Optional[int] = None

Модель продукта содержит следующие поля:

- `title`: Название продукта.
- `description`: Описание продукта (необязательное).
- `price`: Цена продукта.
- `created_at`: Дата создания продукта (необязательное).
- `updated_at`: Дата последнего обновления продукта (необязательное).
- `is_active`: Флаг, указывающий на активность продукта.
- `owner`: Идентификатор владельца продукта (необязательное).

#### Модель корзины
class Cart(BaseModel):
    """Модель корзины"""

    product: List[Product]

Модель корзины содержит:

- `product`: Список продуктов, которые находятся в корзине.

#### Модель токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

Модель токена содержит:

- `access_token`: JWT-токен для авторизации.
- `token_type`: Тип токена (по умолчанию "bearer").

#### Модель данных токена
class TokenData(BaseModel):
    email: str = None

Модель данных токена содержит:

- `email`: Электронный адрес пользователя, который используется для идентификации.

### Использование

Модели пользователя и продукта могут использоваться для:

- Создание и редактирование пользователей.
- Авторизация пользователей.
- Создание и редактирование продуктов.
- Добавление продуктов в корзину.


1.2 **database/db.py**

Этот файл содержит код, отвечающий за подключение к базе данных PostgreSQL в FastAPI-приложении.

### Описание
Код использует библиотеку SQLAlchemy для взаимодействия с базой данных. 
Он создает объект подключения к базе данных, инициализирует сессии 
и предоставляет функцию для получения сессии.

### Функции

#### `get_db`

Функция, отвечающая за получение сессии к базе данных.

- Аргументы:
    - None.
- Действия:
    - Создает новую сессию с помощью `SessionLocal`.
    - Выполняет yield сессии.
    - Закрывает сессию.


1.2 **database/models.py**

код представляет собой набор классов Python, 
использует SQLAlchemy для создания и определения структуры таблиц в базе данных.

### User
- Таблица в БД для хранения информации о пользователях.
- Содержит поля: id, username, email, mobile, password, password2, is_active.

### Product
- Таблица в БД для хранения информации о продуктах.
- Содержит поля: id, title, description, price, created_at, updated_at, is_active, owner.

### Cart
- Таблица в БД для хранения информации о корзине.
- Содержит поля: id, product.

### Зависимости
- SQLAlchemy: необходим для работы с базой данных.
- database.db.Base: базовый класс для всех таблиц, используется для подключения к базе данных.

### Примечание
- В коде используется ForeignKey для установления связи между таблицами.
- Каждая таблица представлена в виде класса.
- Код содержит описание структуры таблиц и их полей.

Этот код представляет собой модели данных для работы с базой данных и может быть использован в приложениях, 
где требуется хранение пользователей, продуктов и корзины.


# **папка utils**

1.1 **utils/auth.py**
1.2 **utils/support_functions.py**



# **./flake8**

### Конфигурация Flake8
Максимальная длина строки max-line-length = 120
Параметр max-line-length в Flake8 определяет максимально допустимую длину строки в вашем коде. 
Строки, превышающие указанную длину, будут вызывать предупреждения.

### Исключенные каталоги и файлы
exclude = migrations, poetry.black, poetry.toml
Параметр exclude в Flake8 позволяет указать каталоги или файлы, которые должны быть исключены из процесса компоновки.
В данном случае это каталог migrations, poetry.файл блокировки и файл poetry.toml исключены из списка.


