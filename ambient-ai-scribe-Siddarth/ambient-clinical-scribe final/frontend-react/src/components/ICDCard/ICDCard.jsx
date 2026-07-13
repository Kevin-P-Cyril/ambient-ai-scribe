import React from 'react'
import { Card, CardContent, Typography, Chip, Stack } from '@mui/material'

export default function ICDCard({ codes = [], editable = false, selectedCodes = [], onSelectionChange }) {
  const selectedSet = new Set(editable ? selectedCodes : [])

  const getCode = (item) => (typeof item === 'string' ? item : item.code || item.title || item.label)
  const getLabel = (item) => {
    if (typeof item === 'string') return item
    return item.description ? `${item.code} — ${item.description}` : item.code || item.title || item.label
  }

  const toggleCode = (code) => {
    if (!onSelectionChange) return
    const next = selectedSet.has(code)
      ? selectedCodes.filter((c) => c !== code)
      : [...selectedCodes, code]
    onSelectionChange(next)
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">ICD Suggestions</Typography>
        <Stack direction="row" spacing={1} sx={{ mt: 1, flexWrap: 'wrap' }}>
          {codes.length ? codes.map((item) => {
            const code = getCode(item)
            const label = getLabel(item)
            const selected = selectedSet.has(code)
            return (
              <Chip
                key={code}
                label={label}
                color={selected ? 'primary' : 'default'}
                clickable={editable}
                onClick={editable ? () => toggleCode(code) : undefined}
                onDelete={editable && selected ? () => toggleCode(code) : undefined}
              />
            )
          }) : <Typography color="text.secondary">No suggestions</Typography>}
        </Stack>
      </CardContent>
    </Card>
  )
}
