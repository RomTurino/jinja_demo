from fastapi import FastAPI
from pydantic import BaseModel
# Создаем экземпляр приложения FastAPI
app = FastAPI()
# Определение базового маршрута


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    '''
    Чтение продукта из базы данных

    **item_id** - идентификатор
    '''
    return {"item_id": item_id}


class Item(BaseModel):
    '''
    Класс продукта

    - **name**: название продукта
    - **price**: цена продукта
    '''
    name: str
    price: float


@app.post("/items/")
async def create_item(item: Item):
    '''
    Создает новый продукт в системе
    - **name**: название продукта
    - **price**: цена продукта
    - **quantity**: количество на складе
    '''
    return {"name": item.name, "price": item.price}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    '''
    Изменяет данные о продукте в системе
    - **name**: название продукта
    - **price**: цена продукта
    '''
    return {"item_id": item_id, "name": item.name, "price": item.price}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    '''
    Удаление продукта из базы данных
    '''
    return {"message": "Item deleted", "item_id": item_id}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10) -> dict:
    '''
    Список продуктов в заданном диапазоне
    - **skip** - начало диапазона
    - **limit** - количество продуктов
    '''
    items = [{"item_id": i} for i in range(skip, skip + limit)]
    return {"items": items}


@app.get("/products/{product_id}")
async def read_product(product_id: int, details: bool = False) -> dict:
    '''
    Вывестти информацию об одном продукте
    - **product_id** - идентификатор продукта в базе данных
    - **details** - если True, то будет показана детальная информация
    '''
    product_info = {"product_id": product_id, "name": f"Product {product_id}"}
    if details:
        product_info["details"] = "Detailed product information"
    return product_info


@app.get("/users/me")
async def read_current_user() -> dict:
    '''Получение информации о текущем пользователе'''
    return {"user": "This is the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int) -> dict:
    '''
    Получение информации о пользователе по его id
    '''
    return {"user_id": user_id, "name": f"User {user_id}"}