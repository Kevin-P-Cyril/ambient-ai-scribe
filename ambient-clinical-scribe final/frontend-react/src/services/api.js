import axios from "axios";

/*
===========================================
Ambient Clinical Scribe API Service
===========================================
*/

const api = axios.create({
    baseURL: "/",
    headers: {
        "Content-Type": "application/json",
    },
});


/* ===========================================================
   HEALTH
=========================================================== */

export const checkHealth = () => api.get("/health");


/* ===========================================================
   AUDIO
=========================================================== */

export const uploadAudio = (formData) =>
    api.post("/upload-audio", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });


/* ===========================================================
   PATIENT
=========================================================== */

export const createPatient = (data) =>
    api.post("/patients", data);

export const getPatients = () =>
    api.get("/patients");


/* ===========================================================
   ENCOUNTERS
=========================================================== */

export const saveEncounter = (patientId, data) =>
    api.post(`/patients/${patientId}/encounters`, data);

export const getEncounters = (patientId) =>
    api.get(`/patients/${patientId}/encounters`);

export const updateEncounter = (encounterId, data) =>
    api.put(`/encounters/${encounterId}`, data);

export const updateEncounterICD = (encounterId, data) =>
    api.put(`/encounters/${encounterId}/icd`, data);


/* ===========================================================
   HISTORY
=========================================================== */

export const getPatientHistory = (patientId) =>
    api.get(`/patients/${patientId}/encounters`);


/* ===========================================================
   EXPORT
=========================================================== */

export const exportPDF = (soapNote) =>
    api.post(
        "/export?format=pdf",
        { soap_note: soapNote },
        {
            responseType: "blob",
        }
    );

export const exportDOCX = (soapNote) =>
    api.post(
        "/export?format=docx",
        { soap_note: soapNote },
        {
            responseType: "blob",
        }
    );


/* ===========================================================
   DEFAULT
=========================================================== */

export default api;