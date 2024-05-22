# TA4 дипломный проект

API backend на Python серивиса "Сервис покупки товаров для авторизованных пользователей". 
В качестве БД PostgreSQL. 
 
**функционал**

1. Регистрация:
ФИО, 
email (уникальный), 
телефон (уникальный), 
пароль
подтверждение пароля.
Все поля обязательны.

2. Пароль 
должен быть не менее 8 символов, 
только латиница, 
минимум 1 символ верхнего регистра,
минимум 1 спец символ $%&!:.

3. Телефон 
должен удовлетворять маске: начинаться с +7 после чего идет 10 цифр.

4. Авторизация: email или телефон (одно поле), пароль
Для авторизованных пользователей доступна таблица товаров, где выводится список всех активных товаров в базе данных

~~5. Товар: name(str), price(int), created_at(datetime), updated_at(datetime), is_active(bool)~~

Доп задача:
Должен быть реализован объект Корзина (list[Товар]), в котором можно через getter получить общую стоимость корзины, 
реализовать методы добавления (одного или нескольких, используя @overload), 
удаления товара\полную очистку Вывод корзины и работу с ней реализовывать не обязательно, достаточно только класса

**Методы доступные неавторизованным пользователям**: регистрация, авторизация
При попытке получить данные без доступа выводить ошибку {code: 401, message:”Unauthorized”}, с HTTP statuscode 401

**Методы доступные авторизованным пользователям**: список пагинированных товаров

Желательно использовать асинхронность

Идентификация пользователя должна происходить по Bearer токену или JWT.
