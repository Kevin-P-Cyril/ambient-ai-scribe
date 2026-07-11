import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'

export default function Transcript({ text = 'No transcript yet' }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Live Transcript</Typography>
        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 1 }}>{text}</Typography>
      </CardContent>
    </Card>
  )
}
