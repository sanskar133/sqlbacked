import { Box, Stack, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { routes } from '../../../../routes/routes';

const HeaderComponent = () => {
	return (
		<div
			style={{
				position: 'sticky',
				top: '0px',
				zIndex: 2,
			}}
		>
			<Box
				display="flex"
				justifyContent="space-between"
				borderBottom="1px solid #fff"
				padding="0px 40px 0px 30px"
				height={60}
				sx={{
					background: '#E4E6F1',
				}}
			>
				<Stack direction="row" gap="12px" alignItems="center">
					<Link style={{ textDecoration: 'none' }} to={routes.home}>
						<Box
							display="flex"
							sx={{ cursor: 'pointer', direction: 'row' }}
							alignItems="center"
						>
							<Box>
								<img
									src="prequel-ai-logo-black.png"
									alt="Aidetic Logo"
									height="60px"
									style={{ marginLeft: '-16px' }}
								/>
							</Box>
						</Box>
					</Link>
				</Stack>
			</Box>
		</div>
	);
};

export default HeaderComponent;
