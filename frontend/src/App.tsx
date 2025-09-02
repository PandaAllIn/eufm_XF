import Box from '@mui/material/Box'

function App() {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Box sx={{ width: '35%', borderRight: '1px solid #e0e0e0', p: 2 }}>
        Source Panel
      </Box>
      <Box sx={{ width: '65%', p: 2 }}>
        Workspace Panel
      </Box>
    </Box>
  )
}

export default App
