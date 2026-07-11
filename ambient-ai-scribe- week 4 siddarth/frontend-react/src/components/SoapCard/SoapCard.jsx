import React from 'react'
import { Card, CardContent, Typography, Button } from '@mui/material'

export default function SoapCard({ soap = {} }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">SOAP Note</Typography>
        <Typography variant="subtitle2" color="text.secondary">Assessment</Typography>
        <Typography sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>{soap.Assessment || soap.assessment || '—'}</Typography>
        <Button variant="outlined">Edit</Button>
      </CardContent>
    </Card>
  )
}
