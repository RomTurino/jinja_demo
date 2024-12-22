
import math
import random
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

available_types_of_animals = ["кот", "пёс", "змея", "попугай", "хомяк", "морская свинья", "обычная свинья"]


class Pet(BaseModel):
    '''
    Класс домашнего питомца

    * type - тип животного ("кот", "пёс", "змея", "попугай", "хомяк", "морская свинья", "обычная свинья")
    * name - кличка животного

    '''
    type: str
    name: str


class User(BaseModel):
    '''
    Класс пользователя

    * name - имя пользователя
    * rating - рейтинг пользователя в системе
    * luck - удача (от 1 до 10)
    '''
    name: str
    rating: int
    luck: int
    pet: Pet


users = [
    {
        "name": f'Хлопчик №{num}',
        "rating": math.factorial(num),
        "luck": random.randint(num, 10),
        "pet" : {
            "type": random.choice(available_types_of_animals),
            "name": f"Животинка {num}"
        }
    }
    for num in range(1, 6)]


app = FastAPI()


@app.get("/")
def get_all_items():
    '''
    Выводит список со всеми пользователями
    '''
    return users


@app.get("/pets")
def get_all_pets():
    '''
    Выводит список со всеми домашними животными
    '''
    return [user["pet"] for user in users]


@app.get("/available_pets")
def get_all_pets():
    '''
    Выводит список c доступными типами животными
    '''
    return available_types_of_animals


@app.post("/create")
def create_person(user:User):
    users.append(user.__dict__)
    return user.__dict__


@app.put("/update/{name}")
def change_person_info(name:str, user:User):
    try:
        index = [user["name"] for user in users].index(name)
        users[index] = user.__dict__
        return "Информация успешно изменена"
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person wasn't found")

@app.delete("delete/{name}")
def delete_person(name:str):
    try:
        index = [user["name"] for user in users].index(name)
        deleted_user = users.pop(index)
        return deleted_user
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person wasn't found")
    


