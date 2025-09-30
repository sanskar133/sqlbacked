import { Skeleton, Typography } from '@mui/material'
import { Box, Stack } from '@mui/system'
import React from 'react'

const ChatSessionLoadingSkeleton = () => {
  return (
    <Box sx={{ maxWidth: 360, margin: 'auto',marginTop: '10px',marginBottom: '20px' }}>
    <Stack spacing={1}>
      
      <Skeleton variant="rectangular" height={40} />
      <Skeleton variant="text" width="60%" />
      <Skeleton variant="rectangular" height={40} />
      <Skeleton variant="text" width="60%" />
    </Stack>
  </Box>
  )
}

export default ChatSessionLoadingSkeleton
