

# to run the API code need to give this command in powershell to run the code ------------ uvicorn <space> name of the file <collon :> name of fastapi fun()<space> --reload, past this in cmd to run this code ----> " uvicorm main:app --reload "


from fastapi import FastAPI , Path , HTTPException ,Query
import json
from pydantic import BaseModel , computed_field , Field 
from typing import Annotated , Optional
from fastapi.responses import JSONResponse # to get json need to import

#--------- CRUD means Create an api endpoint, retrive data using  an api enpoint , Update and delete an API enpoint----
app = FastAPI()
def load_data():
    with open('test.json','r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('test.json','w') as w:
        json.dump(data , w)
#-------------------------- retrive the data API endpoint "Get" -------------------
@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient_ID/{patient_id}")
def Veiw_PatienID(patient_id:str = Path(..., description="please enter the id present in DB")):
    """This is Patient data"""
    data1 = load_data()

    if patient_id in data1:
        return data1[patient_id]
    raise HTTPException(status_code=404 , detail='id not found')

@app.get("/Sort")
def Sorting_Patient(sortby :str = Query(..., description= "sort basis on height , weight and bmi"), order:str = Query("asc", description= " sort in asc or desc order")):
    valid_fields = ['height_cm', 'weight_kg','bmi'] 
    if sortby not in valid_fields:
        return HTTPException(status_code=400 , detail=f"Invalid field selection from {valid_fields}")
    if order not in ["asc","desc"]:
        return HTTPException(status_code=400,detail="Invaild detail")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values() , key=lambda x: x.get(sortby , 0 ), reverse=sort_order)
    return sorted_data

#---------------- Pydantic Model---------------------
class Patient(BaseModel):
    
    id:Annotated[str,Field(..., description= "id of the patient" , examples= ["P001"] )]
    name: Annotated[str,Field(..., description= "Nmae of the patient")]
    age: Annotated[int , Field(gt=0)]
    height_cm:float
    weight_kg:float

    @computed_field
    @property
    def bmi(self)-> float:
        bmi_cal = round((self.weight_kg/(self.height_cm)**2),2)
        return(bmi_cal)
    
#----------------------------- post is use to crate a API endpoint --------------------
@app.post("/create")
def create_patient(patient: Patient):
    
    # load existing data
    data = load_data()
    # check patient already exits
    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Patient already exist")
    #new patient add in database
    data[patient.id] = patient.model_dump(exclude={"id"})

    #save into json
    save_data(data)

    return JSONResponse(status_code=201 ,content= {"message":"Patient details added"} )



#---------------------- crate a Update endpoint "Put" --------------------

class Patient_Update(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[str], Field(default=None,gt=0)]
    height_cm:Annotated[Optional[float] , Field(default=None,gt=0)]
    weight_kg:Annotated[Optional[float], Field(default=None,gt=0)]

@app.put("/edit/{patient_id}")
def update_patient(patient_id : str , patientupdate:Patient_Update):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not fount")
    
    # take the existing patient id

    existing_data = data[patient_id]

    updated_patient_info = patientupdate.model_dump(exclude_unset=True)

    for key , value in update_patient.items():
        existing_data[key] = value

    data[patient_id] = existing_data

    #existing_data -> pydantic object -> updated bmi->pydantic object -> dic
    existing_data['id'] = patient_id
    patient_pydantic_object = Patient(**existing_data)
    # pydantic obj to dict
    existing_data = patient_pydantic_object.model_dump(exclude={'id'})
    # add data to dict
    data[patient_id] = existing_data


    save_data(data)
    return JSONResponse(status_code=200 , content={"message":"update done"})



#------------- create a delete API enpoint "delete"-----------------

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="not found")
    
    del data[patient_id]
    # after deleting we are saving the data
    save_data(data)

    return HTTPException(status_code=200 ,detail="Id deleted")









    

















