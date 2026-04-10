from pydantic import BaseModel , AnyUrl , EmailStr
from typing import List , Dict , Optional , Annotated




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


print(patient_info)
print(address_info)

print(patient_info.address.city)
print(patient_info.address.state)