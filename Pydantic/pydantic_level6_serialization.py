from pydantic import BaseModel , AnyUrl , EmailStr
from typing import List , Dict , Optional , Annotated


#concept:  how we cam export as json or dict

# Condition: Supoose we have a address Gudivada village, bhogapuram mandal, vizinagram district , 531162 and from this i want only city name
class Address(BaseModel):  # child of basemodel
    city: str
    state : str
    pin :  str

class patient(BaseModel):
    name: str
    age: int
    address: Address


address_dict = {"city":"Vizinagram" , "state":"Andhra Pradesh" , "pin":"531162"}

address_info = Address(**address_dict) # Address pydantic object

patient1 = {"name": "Ishwar" , "age": 72 , "address": address_info }

patient_info =  patient(**patient1) # patient pydantic object

temp1 = patient_info.model_dump(include={"name","age"})  # converts pydentic object to dict
print(temp1)
print(type(temp1))

temp2 = patient_info.model_dump(exclude={"name","age"})  # converts pydentic object to dict
print(temp2)
print(type(temp2))


temp3= patient_info.model_dump_json()  # converts pydentic object to dict
print(temp3)
print(type(temp3))


