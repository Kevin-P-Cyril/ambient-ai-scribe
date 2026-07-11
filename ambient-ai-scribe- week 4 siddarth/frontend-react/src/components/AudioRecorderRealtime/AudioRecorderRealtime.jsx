import React, { useRef, useState, useEffect } from 'react'
import { Button, Card, CardContent, Typography } from '@mui/material'

export default function AudioRecorderRealtime({ selectedPatientId = null }) {
  const wsRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const [soapNote, setSoapNote] = useState(null)
  const [icdCodes, setIcdCodes] = useState([])
  const [savedEncounterId, setSavedEncounterId] = useState(null)
  const streamRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const rafRef = useRef(null)
  const canvasRef = useRef(null)

  const [recording, setRecording] = useState(false)
  const [transcript, setTranscript] = useState('')

  useEffect(() => {
    return () => {
      stopAll()
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data)
        if (data.partial) setTranscript(data.partial)
        if (data.final) setTranscript(data.final)
        if (data.soap_note) setSoapNote(data.soap_note)
        if (data.icd_codes) setIcdCodes(data.icd_codes)
        if (data.encounter_id) setSavedEncounterId(data.encounter_id)
        if (data.error) console.error('WS error', data.error)
      } catch (err) {
        console.warn('Non-json ws message', ev.data)
      }
    }
        const data = JSON.parse(ev.data)
        if (data.partial) setTranscript(data.partial)
        if (data.final) setTranscript(data.final)
        if (data.error) console.error('WS error', data.error)
      } catch (err) {
        console.warn('Non-json ws message', ev.data)
      }
    }
    ws.onopen = async () => {
      wsRef.current = ws
      // inform server of selected patient (optional)
      try {
        if (selectedPatientId) wsRef.current.send(JSON.stringify({ patient_id: selectedPatientId }))
      } catch (e) {}
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      const AudioContextClass = window.AudioContext || window.webkitAudioContext
      const ac = new AudioContextClass()
      audioContextRef.current = ac
      const src = ac.createMediaStreamSource(stream)

      const analyser = ac.createAnalyser()
      analyser.fftSize = 2048
      src.connect(analyser)
      analyserRef.current = analyser

      // create script processor to access raw audio data
      const bufferSize = 4096
      const recorderNode = ac.createScriptProcessor(bufferSize, 1, 1)
      recorderNode.onaudioprocess = (e) => {
        const input = e.inputBuffer.getChannelData(0)
        // downsample to 16000
        const down = downsampleBuffer(input, ac.sampleRate, 16000)
        const int16 = floatTo16BitPCM(down)
        try {
          if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(int16.buffer)
          }
        } catch (err) {
          console.error('WS send error', err)
        }
      }
      src.connect(recorderNode)
      recorderNode.connect(ac.destination)
      mediaRecorderRef.current = recorderNode

      drawWaveform()
      setRecording(true)
    }
    ws.onerror = (e) => console.error('WebSocket error', e)
  }

  const stopAll = () => {
    setRecording(false)
    // stop media recorder
    try {
      if (mediaRecorderRef.current) {
        try { mediaRecorderRef.current.disconnect && mediaRecorderRef.current.disconnect() } catch (e) {}
        mediaRecorderRef.current = null
      }
    } catch (e) {}
    // stop tracks
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop())
        streamRef.current = null
      }
    } catch (e) {}
    // close audio context
    try {
      if (audioContextRef.current) {
        audioContextRef.current.close()
        audioContextRef.current = null
      }
    } catch (e) {}
    // stop animation
    try { cancelAnimationFrame(rafRef.current) } catch (e) {}

    // notify server we're done
    try {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send('__done__')
        wsRef.current.close()
      }
    } catch (e) {}
    wsRef.current = null
  }

  function floatTo16BitPCM(float32Array) {
    const l = float32Array.length
    const buf = new Int16Array(l)
    for (let i = 0; i < l; i++) {
      let s = Math.max(-1, Math.min(1, float32Array[i]))
      buf[i] = s < 0 ? s * 0x8000 : s * 0x7fff
    }
    return buf
  }

  function downsampleBuffer(buffer, sampleRate, outSampleRate) {
    if (outSampleRate === sampleRate) return buffer
    const sampleRateRatio = sampleRate / outSampleRate
    const newLength = Math.round(buffer.length / sampleRateRatio)
    const result = new Float32Array(newLength)
    let offsetResult = 0
    let offsetBuffer = 0
    while (offsetResult < result.length) {
      const nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio)
      // use average value between offsets
      let accum = 0, count = 0
      for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
        accum += buffer[i]
        count++
      }
      result[offsetResult] = count ? accum / count : 0
      offsetResult++
      offsetBuffer = nextOffsetBuffer
    }
    return result
  }

  const drawWaveform = () => {
    const canvas = canvasRef.current
    const analyser = analyserRef.current
    if (!canvas || !analyser) return
    const ctx = canvas.getContext('2d')
    const bufferLength = analyser.fftSize
    const dataArray = new Uint8Array(bufferLength)

    const draw = () => {
      rafRef.current = requestAnimationFrame(draw)
      analyser.getByteTimeDomainData(dataArray)
      ctx.fillStyle = '#fafafa'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.lineWidth = 2
      ctx.strokeStyle = '#1976d2'
      ctx.beginPath()
      const sliceWidth = canvas.width / bufferLength
      let x = 0
      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0
        const y = (v * canvas.height) / 2
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
        x += sliceWidth
      }
      ctx.lineTo(canvas.width, canvas.height / 2)
      ctx.stroke()
    }
    draw()
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Live Recorder</Typography>
        <canvas ref={canvasRef} width={600} height={120} style={{ width: '100%', borderRadius: 6, background: '#fafafa' }} />
        <div style={{ marginTop: 12 }}>
          {!recording ? (
            <Button variant="contained" color="primary" onClick={start}>Start</Button>
        </div>
        {soapNote && (
          <div style={{ marginTop: 12 }}>
            <Typography variant="subtitle2">Generated SOAP</Typography>
            <pre style={{ whiteSpace: 'pre-wrap', fontSize: 13 }}>{JSON.stringify(soapNote, null, 2)}</pre>
          </div>
        )}

        {icdCodes && icdCodes.length > 0 && (
          <div style={{ marginTop: 12 }}>
            <Typography variant="subtitle2">ICD Suggestions</Typography>
            <ul>
              {icdCodes.map((c, idx) => (
                <li key={idx}>{c.code} - {c.description || c.label || c.title}</li>
              ))}
            </ul>
          </div>
        )}
        {savedEncounterId && (
          <div style={{ marginTop: 12 }}>
            <Typography variant="subtitle2">Saved</Typography>
            <Typography variant="body2">Encounter ID: {savedEncounterId}</Typography>
          </div>
        )}
          ) : (
            <Button variant="outlined" color="secondary" onClick={stopAll}>Stop</Button>
          )}
        </div>
        <div style={{ marginTop: 12 }}>
          <Typography variant="subtitle2">Live transcript</Typography>
          <Typography variant="body1">{transcript || '(listening...)'}</Typography>
        </div>
      </CardContent>
    </Card>
  )
}
