import React from 'react'
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar } from '@mui/material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import MicIcon from '@mui/icons-material/Mic'
import HistoryIcon from '@mui/icons-material/History'
import { Link as RouterLink } from 'react-router-dom'

const drawerWidth = 240

export default function Sidebar() {
  return (
    <Drawer variant="permanent" sx={{ width: drawerWidth, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' } }}>
      <Toolbar />
      <List>
        <ListItem button component={RouterLink} to="/">
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button component={RouterLink} to="/recording">
          <ListItemIcon>
            <MicIcon />
          </ListItemIcon>
          <ListItemText primary="Recording" />
        </ListItem>
        <ListItem button component={RouterLink} to="/history">
          <ListItemIcon>
            <HistoryIcon />
          </ListItemIcon>
          <ListItemText primary="History" />
        </ListItem>
      </List>
    </Drawer>
  )
}
