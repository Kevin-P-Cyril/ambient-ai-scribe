import React from 'react'
import { Card, CardContent, Typography, Button } from '@mui/material'

export default function UploadArea() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Upload Recording</Typography>
        <input type="file" accept="audio/*" />
        <div style={{ marginTop: 12 }}>
          <Button variant="contained">Upload</Button>
        </div>
      </CardContent>
    </Card>
  )
}
