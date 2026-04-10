from pydantic import BaseModel , AnyUrl , EmailStr , Field , field_validator , model_validator 
from typing import List , Dict , Optional , Annotated

class patient(BaseModel):
    name: str
    age: int
    Email: EmailStr
    weight: float
    married: bool
    allergies:list[str]
    contact_details:Dict[str,str]

# Conditon:  if the age is greater than 60 then the user must contain an Emergency number

    @model_validator(mode= "after")
    def validate_emergency_contact(self):
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError("Patient older than 60 must contain an emergency numbet")
        return self


def patient_type(patient:patient):
    print(patient.name)
    print(patient.age)
    print(patient.Email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("values got updated")


patient1 = {"name": "Ishwar" , "age": 72 , "Email":"ishwarreddy06@hdfc.com" , "weight": 95 , "married":False , "allergies": ["Dust" , "Smoke"],"contact_details":{"mobileNo":"893842382348" , "emergency":"934053489" }}
patient_info =  patient(**patient1)


patient_type(patient_info) 