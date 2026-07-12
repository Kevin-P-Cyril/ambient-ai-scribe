import React, { useEffect, useState } from 'react'
import { FormControl, InputLabel, Select, MenuItem, TextField, Button, Box } from '@mui/material'
import { getPatients, postCreatePatient } from '../../services/api'

export default function PatientSelector({ value, onChange }) {
  const [patients, setPatients] = useState([])
  const [newName, setNewName] = useState('')

  const load = async () => {
    try {
      const res = await getPatients()
      setPatients(res.data || [])
    } catch (e) {
      console.error('Failed to load patients', e)
    }
  }

  useEffect(() => { load() }, [])

  const create = async () => {
    if (!newName) return
    try {
      const res = await postCreatePatient({ name: newName })
      await load()
      setNewName('')
      if (res.data && res.data.id) onChange(res.data.id)
    } catch (e) {
      console.error('Create patient failed', e)
    }
  }

  return (
    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
      <FormControl sx={{ minWidth: 220 }} size="small">
        <InputLabel id="patient-select-label">Patient</InputLabel>
        <Select labelId="patient-select-label" value={value || ''} label="Patient" onChange={(e) => onChange(e.target.value)}>
          <MenuItem value="">(none)</MenuItem>
          {patients.map(p => (
            <MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField size="small" placeholder="New patient name" value={newName} onChange={(e) => setNewName(e.target.value)} />
      <Button variant="outlined" size="small" onClick={create}>Create</Button>
    </Box>
  )
}
