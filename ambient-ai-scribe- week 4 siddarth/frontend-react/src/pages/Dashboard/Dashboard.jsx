import React from 'react'
import { Grid, Card, CardContent, Typography } from '@mui/material'
import AudioRecorder from '../../components/AudioRecorder/AudioRecorder'
import Transcript from '../../components/Transcript/Transcript'
import SoapCard from '../../components/SoapCard/SoapCard'
import ICDCard from '../../components/ICDCard/ICDCard'

export default function Dashboard() {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={8}>
        <AudioRecorder />
        <Transcript text={'(Live transcript will appear here)'} />
      </Grid>
      <Grid item xs={12} md={4}>
        <SoapCard />
        <div style={{ height: 12 }} />
        <ICDCard />
      </Grid>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6">Today's Patients</Typography>
            <Typography color="text.secondary">Placeholder metrics and charts</Typography>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  )
}
