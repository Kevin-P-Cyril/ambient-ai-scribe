import { createTheme } from '@mui/material/styles'

const lightPalette = {
  primary: { main: '#2563EB' },
  secondary: { main: '#3B82F6' },
  background: { default: '#F8FAFC', paper: '#FFFFFF' },
  text: { primary: '#1E293B', secondary: '#6B7280' },
  success: { main: '#16A34A' },
  warning: { main: '#F59E0B' }
}

const theme = createTheme({
  palette: {
    mode: 'light',
    ...lightPalette
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: { borderRadius: 14 }
      }
    }
  }
})

export default theme
