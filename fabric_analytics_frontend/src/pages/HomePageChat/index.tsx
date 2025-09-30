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
			localStorage.setItem('user_id', accessId.trim());
			navigate(routes.chat);
		}
	};

	return (
		<Box sx={{ padding: '30px 30px 30px 30px' }}>
			<Stack direction="row" gap="12px" alignItems="center">
				<Box display="flex" sx={{ cursor: 'pointer' }} alignItems="center">
					<img
						src="prequel-ai-logo-black.png"
						alt="Prequel AI Logo"
						height="60px"
						style={{ borderRadius: '4px', marginRight: '8px' }}
					/>
				</Box>

				{/* <Typography variant="customPrmH6Bold" lineHeight="24px">
					Aidetic | PrequelAI
				</Typography> */}
			</Stack>
			<Stack height="calc(100vh - 128.44px)" alignItems="center" justifyContent="center">
				<Stack
					gap="30px"
					alignItems="center"
					justifyContent="center"
					width="40%"
					minWidth="350px"
				>
					<form
						noValidate
						autoComplete="off"
						style={{ width: '100%' }}
						onSubmit={handleAccessChat}
					>
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
						<Button
							size="medium"
							variant="contained"
							color="primary"
							sx={{ width: '100%', height: '56px', marginTop: '30px' }}
							onClick={handleAccessChat}
						>
							Access
						</Button>
					</form>
				</Stack>
			</Stack>
		</Box>
	);
}

export default HomePageChat;
