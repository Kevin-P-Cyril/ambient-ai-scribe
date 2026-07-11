import axios from 'axios'

const api = axios.create({ baseURL: '/' })

export const postTranscribe = (form) => api.post('/transcribe', form)
export const postGenerateSoap = (data) => api.post('/generate-soap', data)
export const postIcdSearch = (data) => api.post('/icd-search', data)
export const postUpload = (form) => api.post('/upload', form)
export const getHistory = () => api.get('/history')
export const getPatients = () => api.get('/patients')
export const postCreatePatient = (data) => api.post('/patients', data)
export const postSaveEncounter = (patientId, data) => api.post(`/patients/${patientId}/encounters`, data)
export const getEncounters = (patientId) => api.get(`/patients/${patientId}/encounters`)
export const putUpdateEncounter = (encounterId, data) => api.put(`/encounters/${encounterId}`, data)
export const putUpdateEncounterIcd = (encounterId, data) => api.put(`/encounters/${encounterId}/icd`, data)
export const postExportPdf = (data) => api.post('/export?format=pdf', data, { responseType: 'blob' })

export default api
