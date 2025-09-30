import { Box, Button, Grid, Typography } from '@mui/material';
import React from 'react';

class ErrorFallback extends React.Component {
	render() {
		return (
			<Grid container justifyContent="center" alignItems="center" sx={{ height: '30vh' }}>
				<Box textAlign="center">
					<Typography>Something went wrong!</Typography>
					<Button
						onClick={() => window.location.reload()}
						variant="contained"
						color="primary"
					>
						Refresh
					</Button>
				</Box>
			</Grid>
		);
	}
}

export default ErrorFallback;
