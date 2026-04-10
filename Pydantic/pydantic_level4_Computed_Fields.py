from pydantic import BaseModel , AnyUrl , EmailStr , computed_field
from typing import List , Dict , Optional , Annotated

class patient(BaseModel):
    name: str
    age: int
    Email: EmailStr
    weight: float
    height: float
    married: bool
    allergies:list[str]
    contact_details:Dict[str,str]

 # Condition : Add BMI value using height and weight
    @computed_field
    @property
    def bmi(self) -> float: 
        bmi1 = round(self.weight/(self.height**2),2)
        return bmi1





def patient_type(patient:patient):
    print(patient.name)
    print(patient.age)
    print(patient.Email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("BMI" , patient.bmi)
    print("values got updated")


patient1 = {"name": "Ishwar" , "age": 72 , "Email":"ishwarreddy06@hdfc.com" , "weight": 95.5 ,"height":1.72, "married":False , "allergies": ["Dust" , "Smoke"],"contact_details":{"mobileNo":"893842382348" , "emergency":"934053489" }}
patient_info =  patient(**patient1)


patient_type(patient_info) 