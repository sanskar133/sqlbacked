import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import CustomInput from '../../components/shared/CustomInput';
import React, { useState } from 'react';
import { TEXT_CONSTANTS } from '../../utils/TextContants';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { routes } from '../../routes/routes';
import { ACCESS_LIST } from '../../utils/utilFunctions';
import _ from 'lodash';

function HomePageChat() {
	const navigate = useNavigate();
	const [accessId, setAccessId] = useState<string>('');
	const [accessIdError, setAccessIdError] = useState<string>('');
	const [password, setPassword] = useState<string>('');
	const [passwordError, setPasswordError] = useState<string>('');

	const handleAccessChat = (e: React.SyntheticEvent) => {
		e.preventDefault();

		if (accessId.trim() === '') {
			setAccessIdError('Access code is required!');
		} else if (
			!_.some(ACCESS_LIST, (item) => {
				return item === accessId.trim().split('.')[0];
			})
		) {
			setAccessIdError('Not Authorized!');
		} else {
			setAccessIdError('');
			setPasswordError('');
			localStorage.setItem('user_id', accessId.trim());
			navigate(routes.chat);
		}
	};

	return (
		<Box
			sx={{
				minHeight: '100vh',
				background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
				padding: '20px',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
			}}
		>
			<Box
				sx={{
					backgroundColor: 'rgba(255, 255, 255, 0.95)',
					backdropFilter: 'blur(10px)',
					borderRadius: '20px',
					padding: '50px 40px',
					boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
					width: '100%',
					maxWidth: '450px',
					textAlign: 'center',
				}}
			>
				<Typography
					variant="h3"
					sx={{
						marginBottom: '10px',
						fontWeight: 'bold',
						color: '#2c3e50',
						fontSize: '2rem',
					}}
				>
					Welcome Back
				</Typography>
				<Typography
					variant="body1"
					sx={{
						marginBottom: '40px',
						color: '#7f8c8d',
						fontSize: '1.1rem',
					}}
				>
					Sign in to access your AI assistant
				</Typography>

				<form onSubmit={handleAccessChat} style={{ width: '100%' }}>
					<Stack spacing={3}>
						<CustomInput
							value={accessId}
							setValue={(val) => {
								setAccessId(val);
								setAccessIdError('');
							}}
							fullWidth
							size="medium"
							placeholder={TEXT_CONSTANTS.HOME_PAGE_CHAT_PLACEHOLDER}
							helperText={accessIdError}
							error={accessIdError !== ''}
						/>

						<CustomInput
							value={password}
							setValue={(val) => {
								setPassword(val);
								setPasswordError('');
							}}
							fullWidth
							size="medium"
							placeholder="Password"
							helperText={passwordError}
							error={passwordError !== ''}
							type="password"
						/>

						<Button
							type="submit"
							variant="contained"
							sx={{
								width: '100%',
								height: '56px',
								marginTop: '20px',
								background: '#000000',
								fontSize: '1.1rem',
								fontWeight: 'bold',
								textTransform: 'none',
								borderRadius: '12px',
								boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
								color: '#ffffff',
								'&:hover': {
									background: '#333333',
									boxShadow: '0 6px 20px rgba(0, 0, 0, 0.3)',
								},
							}}
						>
							Access Chat
						</Button>
					</Stack>
				</form>

				<Typography
					variant="body2"
					sx={{
						marginTop: '30px',
						color: '#95a5a6',
						fontSize: '0.9rem',
					}}
				>
					Powered by Prequel AI
				</Typography>
			</Box>
		</Box>
	);
}

export default HomePageChat;
