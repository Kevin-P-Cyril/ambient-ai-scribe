from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# =====================================================
# SOAP NOTE
# =====================================================

class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str


# =====================================================
# PATIENT
# =====================================================

class PatientCreate(BaseModel):
    name: str
    metadata: Optional[Dict[str, Any]] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: str


# =====================================================
# ENCOUNTER
# =====================================================

class EncounterCreate(BaseModel):
    patient_id: int
    transcript: str
    soap: SOAPNote
    icd_codes: List[Dict[str, Any]] = Field(default_factory=list)


class EncounterUpdate(BaseModel):
    transcript: Optional[str] = None
    soap: Optional[SOAPNote] = None
    icd_codes: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None


class FinalizeEncounter(BaseModel):
    encounter_id: int
    final_soap: SOAPNote


# =====================================================
# EXPORT
# =====================================================

class ExportRequest(BaseModel):
    encounter_id: int
    format: str = "pdf"


# =====================================================
# API RESPONSE
# =====================================================

class APIResponse(BaseModel):
    success: bool
    message: str


# =====================================================
# HISTORY
# =====================================================

class EncounterHistory(BaseModel):
    id: int
    transcript: str
    soap: Optional[SOAPNote] = None
    ai_soap: Optional[SOAPNote] = None
    final_soap: Optional[SOAPNote] = None
    icd_codes: Optional[List[Dict[str, Any]]] = None
    status: str
    created_at: str
    updated_at: Optional[str] = None
    finalized_at: Optional[str] = None