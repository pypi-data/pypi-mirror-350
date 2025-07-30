from pydantic import BaseModel
from typing import Literal, List, Dict, Optional

    
class NLUInput(BaseModel):
    rawText: str
    
    
NERResult = Dict[str, str]
    
    
    
class CLSResult(BaseModel):
    label: str 
    score: float
         
         
class ParserResult(BaseModel):
    domain: str
    intention: str
    ner:  Dict[str, str]
    

class Slot(BaseModel):
    raw_value: str
    value: str
    
class Event(BaseModel):
    eventId: str
    raw: ParserResult
    score: float = 1.0
    slots: Dict[str, Slot]
    
    
class ParserOutput(BaseModel):
    code: Literal[0, 1] = 0
    data: List[Event]
    message: str = "success"
    
    
class HealthCheckOutput(BaseModel):
    code: Literal[0, 1] = 0
    message: str = "success"
    
    
class DomainResult(BaseModel):
    domain: str 
    probability: float
    session: Dict[str, str] = {}
    
    
class DomainOutput(BaseModel):
    code: Literal[0, 1] = 0
    data: DomainResult
    message: str = "success"