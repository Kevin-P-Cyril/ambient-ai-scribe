import React, { useEffect, useState } from 'react'
import { Paper, Typography, List, ListItem, ListItemText, Divider, Button, TextField, Box } from '@mui/material'
import PatientSelector from '../../components/PatientSelector/PatientSelector'
import ICDCard from '../../components/ICDCard/ICDCard'
import { getEncounters, putUpdateEncounterIcd, putUpdateEncounter } from '../../services/api'

export default function History() {
  const [patientId, setPatientId] = useState(null)
  const [encounters, setEncounters] = useState([])
  const [editingId, setEditingId] = useState(null)
  const [editedSoap, setEditedSoap] = useState({})
  const [editedIcdCodes, setEditedIcdCodes] = useState([])

  useEffect(() => {
    const load = async () => {
      if (!patientId) return setEncounters([])
      try {
        const res = await getEncounters(patientId)
        setEncounters(res.data || [])
      } catch (e) {
        console.error('Failed to load encounters', e)
        setEncounters([])
      }
    }
    load()
  }, [patientId])

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6">Patient History</Typography>
      <PatientSelector value={patientId} onChange={setPatientId} />

      {!patientId && (
        <Typography color="text.secondary">Select a patient to view encounters</Typography>
      )}

      {patientId && (
        <List>
          {encounters.length === 0 && (
            <ListItem><ListItemText primary="No encounters found" /></ListItem>
          )}
          {encounters.map(enc => (
            <React.Fragment key={enc.id}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={enc.created_at}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">Transcript:</Typography>
                      <div style={{ whiteSpace: 'pre-wrap' }}>{enc.transcript}</div>

                      <Box sx={{ mt: 1 }}>
                        <Typography component="span" variant="body2" color="text.primary">SOAP:</Typography>
                        {editingId === enc.id ? (
                          <Box sx={{ display: 'grid', gap: 1, mt: 1 }}>
                            <TextField label="Subjective" multiline size="small" value={editedSoap.subjective || ''} onChange={(e) => setEditedSoap(prev => ({ ...prev, subjective: e.target.value }))} />
                            <TextField label="Objective" multiline size="small" value={editedSoap.objective || ''} onChange={(e) => setEditedSoap(prev => ({ ...prev, objective: e.target.value }))} />
                            <TextField label="Assessment" multiline size="small" value={editedSoap.assessment || ''} onChange={(e) => setEditedSoap(prev => ({ ...prev, assessment: e.target.value }))} />
                            <TextField label="Plan" multiline size="small" value={editedSoap.plan || ''} onChange={(e) => setEditedSoap(prev => ({ ...prev, plan: e.target.value }))} />
                            <Typography variant="subtitle2" sx={{ mt: 1 }}>ICD Selection</Typography>
                            <ICDCard codes={enc.icd_codes || []} editable selectedCodes={editedIcdCodes} onSelectionChange={setEditedIcdCodes} />
                            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                              <Button variant="contained" size="small" onClick={async () => {
                                try {
                                  await putUpdateEncounter(enc.id, { soap: editedSoap, icd_codes: editedIcdCodes })
                                  const res = await getEncounters(patientId)
                                  setEncounters(res.data || [])
                                  setEditingId(null)
                                } catch (e) {
                                  console.error('Save failed', e)
                                }
                              }}>Save Note</Button>
                              <Button variant="outlined" size="small" onClick={async () => {
                                try {
                                  await putUpdateEncounterIcd(enc.id, { icd_codes: editedIcdCodes })
                                  const res = await getEncounters(patientId)
                                  setEncounters(res.data || [])
                                } catch (e) {
                                  console.error('ICD save failed', e)
                                }
                              }}>Save ICDs</Button>
                              <Button variant="text" size="small" onClick={() => setEditingId(null)}>Cancel</Button>
                            </Box>
                          </Box>
                        ) : (
                          <>
                            <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(enc.soap, null, 2)}</pre>
                            <Typography variant="subtitle2" sx={{ mt: 1 }}>ICD Codes</Typography>
                            <ICDCard codes={enc.icd_codes || []} selectedCodes={enc.icd_codes ? enc.icd_codes.map(c => c.code || c) : []} />
                            <Button size="small" onClick={() => { setEditingId(enc.id); setEditedSoap(enc.soap || {}); setEditedIcdCodes(enc.icd_codes ? enc.icd_codes.map(c => c.code || c) : []) }}>Edit</Button>
                          </>
                        )}
                      </Box>
                    </>
                  }
                />
              </ListItem>
              <Divider component="li" />
            </React.Fragment>
          ))}
        </List>
      )}
    </Paper>
  )
}
