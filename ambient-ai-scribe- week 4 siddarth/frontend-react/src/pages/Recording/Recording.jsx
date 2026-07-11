import React from 'react'
import { Grid } from '@mui/material'
import AudioRecorderRealtime from '../../components/AudioRecorderRealtime/AudioRecorderRealtime'
import Transcript from '../../components/Transcript/Transcript'
import PatientSelector from '../../components/PatientSelector/PatientSelector'
import { useState } from 'react'

export default function Recording() {
  const [selectedPatient, setSelectedPatient] = useState(null)
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={8}>
        <PatientSelector value={selectedPatient} onChange={setSelectedPatient} />
        <AudioRecorderRealtime selectedPatientId={selectedPatient} />
        <Transcript />
      </Grid>
    </Grid>
  )
}
