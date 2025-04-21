from pydantic import BaseModel
from datetime import datetime
from typing import List


class CarData(BaseModel):
    auction_name:str
    auction_date:datetime
    title:str
    price:float
    year:int
    mileage:str
    feul:str
    entry:int
    mission:str
    score:str
    images:List[str]







