from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, Union

class CreateResource(BaseModel):
    hospital_name: Annotated[str, Field(examples=["Fatima Jinnah Hospital"])]
    hospital_username: Annotated[str, Field(examples=["mayo"])]
    icu_beds: Annotated[int, Field(examples=["1"], default=0)]
    ventilators: Annotated[int, Field(examples=["1"], default=0)]
    monitors: Annotated[int, Field(examples=["1"], default=0)]
    defibrillators: Annotated[int, Field(examples=["1"], default=0)]
    infusion_pumps: Annotated[int, Field(examples=["1"], default=0)]
    oxygen_cylinders: Annotated[int, Field(examples=["1"], default=0)]
    xray_machines: Annotated[int, Field(examples=["1"], default=0)]
    ultrasound_machines: Annotated[int, Field(examples=["1"], default=0)]
    ct_scanners: Annotated[int, Field(examples=["1"], default=0)]
    mri_machines: Annotated[int, Field(examples=["1"], default=0)]
    ecg_machines: Annotated[int, Field(examples=["1"], default=0)]
    dialysis_machines: Annotated[int, Field(examples=["1"], default=0)]

    model_config = ConfigDict(from_attributes=True)

class ReadResource(CreateResource):
    
    # id:int 
    id: Union[str, int] = Field(examples=["1"])
    hospital_name: Union[str, int] = Field(examples=["Fatima Jinnah Hospital"], default=None)
    hospital_username: Annotated[str, Field(examples=["mayo"])]
    icu_beds: Union[str, int] = Field(examples=["1"], default=0)
    ventilators: Union[str, int] = Field(examples=["1"], default=0)
    monitors: Union[str, int] = Field(examples=["1"], default=0)
    defibrillators: Union[str, int] = Field(examples=["1"], default=0)
    infusion_pumps: Union[str, int] = Field(examples=["1"], default=0)
    oxygen_cylinders: Union[str, int] = Field(examples=["1"], default=0)
    xray_machines: Union[str, int] = Field(examples=["1"], default=0)
    ultrasound_machines: Union[str, int] = Field(examples=["1"], default=0)
    ct_scanners: Union[str, int] = Field(examples=["1"], default=0)
    mri_machines: Union[str, int] = Field(examples=["1"], default=0)
    ecg_machines: Union[str, int] = Field(examples=["1"], default=0)
    dialysis_machines: Union[str, int] = Field(examples=["1"], default=0)

    model_config = ConfigDict(from_attributes=True)

class UpdateResource(CreateResource):
    hospital_name: Optional[str] = Field(default=None, examples=["Fatima Jinnah Hospital"])
    icu_beds: Optional[int]  = Field(default=None, examples=["1"])
    ventilators: Optional[int] = Field(default=None, examples=["1"])
    monitors: Optional[int] = Field(default=None, examples=["1"])
    defibrillators: Optional[int] = Field(default=None, examples=["1"])
    infusion_pumps: Optional[int] = Field(default=None, examples=["1"])
    oxygen_cylinders: Optional[int] = Field(default=None, examples=["1"])
    xray_machines: Optional[int] = Field(default=None, examples=["1"])
    ultrasound_machines: Optional[int] = Field(default=None, examples=["1"])
    ct_scanners: Optional[int] = Field(default=None, examples=["1"])
    mri_machines: Optional[int] = Field(default=None, examples=["1"])
    ecg_machines: Optional[int] = Field(default=None, examples=["1"])
    dialysis_machines: Optional[int] = Field(default=None, examples=["1"])

    model_config = ConfigDict(from_attributes=True)
    
