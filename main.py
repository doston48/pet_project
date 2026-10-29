from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="pet project api ")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pets = [
    {"id": 1, "name": "Biscuit", "species": "Dog", "age": 2,
     "bio": "Loves belly rubs and long walks.", "adopted": False},
    {"id": 2, "name": "Luna", "species": "Cat", "age": 1,
     "bio": "A curious kitten who loves cardboard boxes.", "adopted": False},
    {"id": 3, "name": "Peanut", "species": "Rabbit", "age": 3,
     "bio": "Calm and gentle, great with kids.", "adopted": False},
]
next_pet_id = 4
requests = []
next_request_id = 1
class Pet(BaseModel):
    name: str
    species: str
    age: int
    bio: str 
    
    
class Request(BaseModel):
    request_name: str
    message: str

@app.get("/")
def home():
    return{"message": "pet api is running"}

@app.get("/pets")
def get_pets():
    return pets

@app.get("/pets/{pet_id}")
def get_pet(pet_id: int):
    for pet in pets:
        if pet["id"] == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Not Found")

@app.post("/pets")
def add_pet(pet: Pet):
    global next_pet_id 
    new_pet = {
        "id": next_pet_id,
        "name": pet.name,
        "species": pet.species,
        "age": pet.age,
        "bio": pet.bio,
        "adopted": False,
    }
    pets.append(new_pet)
    next_pet_id +=1
    return new_pet


@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    for pet in pets:
        if pet["id"] == pet_id:
            pets.remove(pet)
            return {"message":"pet removed from shelter"}
    raise HTTPException(status_code=404, detail="not found")


@app.patch("/requests/{request_id}/reject")
def reject_request(request_id: int):
    for request in requests:
        if request["id"] == request_id:
            request["status"] = "rejected"
            return request
    raise HTTPException(status_code=404,detail="not found")            