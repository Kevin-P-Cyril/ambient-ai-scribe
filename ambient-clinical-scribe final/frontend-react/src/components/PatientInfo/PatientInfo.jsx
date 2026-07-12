import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'

export default function PatientInfo({ patient = {} }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Patient</Typography>
        <Typography variant="body2" color="text.secondary">{patient.name || 'Unknown'}</Typography>
      </CardContent>
    </Card>
  )
}
