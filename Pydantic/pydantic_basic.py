from pydantic import BaseModel

class patient(BaseModel):
    name:str
    age:int

def patient_type(patient:patient):
    print(patient.name)
    print(patient.age)
    print("values got updated")


patient1 = {"name": "Ishwar" , "age":26}
patient_info =  patient(**patient1)


patient_type(patient_info)