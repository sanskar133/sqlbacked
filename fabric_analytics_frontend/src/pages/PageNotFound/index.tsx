import { Box, Button, Typography } from '@mui/material';

const PageNotFound: any = () => {
	return (
		<Box
			height="100vh"
			sx={{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
			}}
		>
			<Box
				sx={{
					textAlign: 'center',
					//margin: 'auto',
					fontSize: '50px',
					//marginTop: '50px',
				}}
			>
				Uh-Oh...{' '}
				<Typography>
					The page you are looking for may have been moved, deleted or possibly never
					existed.
				</Typography>
				<Typography sx={{ fontSize: '100px', color: '#a1a1a1', marginTop: '80px', mb: 5 }}>
					404
				</Typography>
				<Box display="flex" justifyContent="center" mt={2}>
					<Button
						variant="contained"
						onClick={() => {
							window.location.href = '/';
						}}
					>
						Home
					</Button>
				</Box>
			</Box>
		</Box>
	);
};

export default PageNotFound;
