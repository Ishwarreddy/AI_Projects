from pydantic import BaseModel , AnyUrl , EmailStr , Field

#use pip install 'pydantic[email]' to install email validation modeule
#Field is used for validation, like age should not be negative , weight should not be negative and also used to add meta data

from typing import List , Dict , Optional , Annotated

# annotated and Field both combine to give meta data

class patient(BaseModel):
    name: Annotated[str,Field(max_length=50, title="Name of the patient" , description="give the name of the patient less than 50 charaters" , examples=["Ishwar", "Op_Raavan"])]
    age:int = Field(gt=0)
    Email: EmailStr
    linkdin_url : AnyUrl
    weight: float = Field(gt=0)
    married: Optional[bool]
    allergies:Optional[list[str]]
    contact_details:Dict[str,str]

def patient_type(patient:patient):
    print(patient.name)
    print(patient.age)
    print(patient.Email)
    print(patient.linkdin_url)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("values got updated")


patient1 = {"name": "Ishwar" , "age":26 , "Email":"ishwarreddy06@gmail.com" ,"linkdin_url":"https://in.linkedin.com/", "weight": 95 , "married":False , "allergies": ["Dust" , "Smoke"],"contact_details":{"mobileNo":"893842382348"} }
patient_info =  patient(**patient1)


patient_type(patient_info)