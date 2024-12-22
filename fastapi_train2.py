
from enum import Enum
import math
import random
from typing import Annotated, Literal

from fastapi import Body, FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

available_types_of_animals = ["кот", "пёс", "рыбка", "попугай", "хомяк", "морская свинья", "обычная свинья"]
example_user = lambda : {
                "name": f'Хлопчик №{random.randint(1,5)}',
                "rating": random.randint(1,25),
                "luck": random.randint(1, 10),
                "pet": {
                        "type":"кот",
                        "name": f"Животинка {random.randint(1,5)}"
                    },
            }
   

class AnimalType(str, Enum):
    CAT = "кот"
    DOG = "пёс"
    SNAKE = "рыбка"
    PARROT = "попугай"
    HUMSTER = "хомяк"
    GUINEA_PIG = "морская свинья"
    PIG = "обычная свинья"


class Pet(BaseModel):
    '''
    Класс домашнего питомца

    * type - тип животного ("кот", "пёс", "рыбка", "попугай", "хомяк", "морская свинья", "обычная свинья")
    * name - кличка животного

    '''
    type: Annotated[
        AnimalType,
        Field(
            title="Тип животного",
            description="Доступные типы животных",
            default=random.choice(list(AnimalType)),
        ),
    ]
    name: str = Field(title="кличка животного", examples=[f"Животинка {random.randint(1,100)}"])


class User(BaseModel):
    '''
    Класс пользователя

    * name - имя пользователя
    * rating - рейтинг пользователя в системе
    * luck - удача (от 1 до 10)
    '''
    name: str = Field(title="имя пользователя", examples=[f"Хлопчик №{random.randint(1,5)}"])
    rating: int = Field(title="рейтинг пользователя", default=random.randint(1,25))
    luck: int = Field(title="удача пользователя", default=random.randint(1,10))
    pet:Pet

    

users = [
    {
        "name": f'Хлопчик №{num}',
        "rating": math.factorial(num),
        "luck": random.randint(num, 10),
        "pet" : {
            "type": random.choice(list(AnimalType)),
            "name": f"Животинка {num}"
        }
    }
    for num in range(1, 6)]




app = FastAPI(
    title="UrbanPeople API",
    description="UrbanPeople API helps you to work with the list of people in CPU memory. 🚀",
    version="0.0.1",
    contact={
        "name": "Urban University",
        "url": "https://urban-university.ru/#consult",
        "email": "help@it-university.pro",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users."
        },
        {
            "name":"pets",
            "description": "operations with pets"
        }
    ]
)


@app.get("/", tags=["users"])
def get_all_items():
    '''
    Выводит список со всеми пользователями
    '''
    
    return JSONResponse(content=users, media_type="application/json; charset=utf-8")


@app.get("/pets", tags=["pets"])
def get_all_pets():
    '''
    Выводит список со всеми домашними животными
    '''
    return [user["pet"] for user in users]


@app.get("/available_pets", tags=["pets"])
def get_all_pets():
    '''
    Выводит список c доступными типами животными
    '''
    return list(AnimalType)


@app.post("/create", tags=["users"])
def create_person(
    user: Annotated[
            User,
            Body(
                examples=[
                    example_user()
                ]  # Пример структуры пользователя
            ),
        ]
    ):
    users.append(user.__dict__)
    return user.__dict__


@app.put("/update/{name}", tags=["users"])
def change_person_info(
        name: Annotated[
            str,
            Path(
                title="Имя пользователя",
                description="Имя пользователя, информацию о котором необходимо изменить",
            ),
        ],
        user: Annotated[
            User,
            Body(
                examples=[example_user()]
            ),
        ]
    ):

    try:
        index = [user["name"] for user in users].index(name)
        users[index] = user.__dict__
        return "Информация успешно изменена"
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person wasn't found")

@app.delete("/delete/{name}", tags=["users"])
def delete_person(
        name: Annotated[
            str,
            Path(
                title="Имя пользователя",
                description="Имя пользователя, которого необходимо удалить",
            ),
        ]
    ):
    try:
        index = [user["name"] for user in users].index(name)
        deleted_user = users.pop(index)
        return deleted_user
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person wasn't found")
    


