import { Box } from '@mui/material';
import LinearProgress from '@mui/material/LinearProgress';

const index = () => {
	return (
		<Box
			sx={{
				position: 'fixed',
				top: '0',
				right: '0',
				left: '0',
				bottom: '0',
				zIndex: '1000',
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				justifyContent: 'center',
			}}
		>
			<Box
				sx={{
					width: '70%',
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					justifyContent: 'center',
				}}
			>
				<Box
					sx={{
						width: '100%',
						textAlign: 'center',
						margin: 'auto',
						mt: 6,
					}}
				>
					<LinearProgress color="warning" />
				</Box>
			</Box>
		</Box>
	);
};

export default index;
