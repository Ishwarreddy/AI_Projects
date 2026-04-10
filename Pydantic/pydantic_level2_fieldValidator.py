from pydantic import BaseModel , AnyUrl , EmailStr , Field , field_validator 
from typing import List , Dict , Optional , Annotated

class patient(BaseModel):
    name: str
    age: int
    Email: EmailStr
    weight: float
    married: bool
    allergies:list[str]
    contact_details:Dict[str,str]


    # conditon , only accpet the mail contain HDFC and ICICI mails

    @field_validator("Email")
    @classmethod
    def email_validator(cls , value):
        valid_domain = ["hdfc.com" , "icici.com"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domain:
            raise ValueError ("Not a valid domain")
        return value
    
    # to get the name in uppercase

    @field_validator("name")
    @classmethod
    def tranformer_name(cls , value):
        return value.upper() # output : ishwar ----> ISHWAR
    

    

def patient_type(patient:patient):
    print(patient.name)
    print(patient.age)
    print(patient.Email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("values got updated")


patient1 = {"name": "Ishwar" , "age":26 , "Email":"ishwarreddy06@hdfc.com" , "weight": 95 , "married":False , "allergies": ["Dust" , "Smoke"],"contact_details":{"mobileNo":"893842382348"} }
patient_info =  patient(**patient1)


patient_type(patient_info)