import React from 'react'
import { Card, CardContent, Typography, Button } from '@mui/material'

export default function AudioRecorder() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Live Recorder</Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Start/stop recording and view live waveform (placeholder)
        </Typography>
        <Button variant="contained">Start</Button>
      </CardContent>
    </Card>
  )
}
