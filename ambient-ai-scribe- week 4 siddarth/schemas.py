from pydantic import BaseModel

class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str