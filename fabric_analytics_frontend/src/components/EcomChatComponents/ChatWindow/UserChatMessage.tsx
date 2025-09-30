import { Divider, Typography } from '@mui/material';
import { Box } from '@mui/system';
import moment from 'moment';
import PersonIcon from '@mui/icons-material/Person';

const UserChatMessage = ({
	message,
	created_at,
}: {
	message: string;
	created_at: undefined | string;
}) => {
	return (
		<>
			<Box display="flex" mb="10px" alignItems="flex-start">
				<span
					style={{
						minWidth: '25px',
						minHeight: '25px',
						borderRadius: '5px',
						backgroundColor: '#9b59b6',
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
					}}
				>
					<PersonIcon sx={{ fontSize: '18px', color: 'white' }} />
				</span>
				<Box>
					<Typography ml="20px" fontWeight="600" variant="body1">
						You
					</Typography>
					<Typography ml="20px" fontWeight="400" mt="20px" variant="h6">
						{message}
					</Typography>
					<Typography
						ml="20px"
						mt="10px"
						sx={{
							color: 'rgba(94, 84, 104, 0.75)',
							fontSize: '11px',
							fontStyle: 'normal',
							fontWeight: 400,
							lineHeight: '110%',
							letterSpacing: '-0.11px',
						}}
					>
						{moment(created_at).format('ddd MMM D, YYYY')} at{' '}
						{moment(created_at).format('hh:mm:ss a')}
					</Typography>
				</Box>
			</Box>

			<Divider sx={{ margin: '20px 0px', ml: '44px', mb: '34px' }} light />
		</>
	);
};

export default UserChatMessage;
