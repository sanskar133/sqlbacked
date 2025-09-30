import { Box } from '@mui/system';
import { SvgChatBotSideIcon } from '../../shared/AppIcons';
import { CircularProgress, Divider, Typography } from '@mui/material';

import TableLoadingSkeleton from '../../shared/TableLoadingSkeleton/TableLoadingSkeleton';

const BotChatMessage = ({
	message,
	isProcessing,
	processingMessage,
}: {
	message: any;
	isProcessing: boolean;
	processingMessage?: string;
}) => {
	return (
		<>
			<Box sx={{ position: 'relative' }} display="flex" alignItems="flex-start">
				<Box>
					<img
						src="favicon-32x32.png"
						alt="Aidetic Logo"
						height="25px"
						width="25px"
						style={{
							borderRadius: '6px',
							backgroundColor: '#05445E',
							paddingBottom: '2.5px',
							paddingLeft: '2px',
						}}
					/>
				</Box>
				<Box sx={{ width: '100%' }} ml="20px">
					<Box sx={{ display: 'flex', alignItems: 'start', mb: '20px' }}>
						<Typography fontWeight="600" variant="body1">
							PrequelAI
						</Typography>

						{isProcessing && (
							<CircularProgress
								sx={{ marginTop: '6px', marginLeft: '15px' }}
								size={14}
							/>
						)}
						<Typography mx="10px" fontWeight="400" variant="h6">
							{processingMessage}
						</Typography>
					</Box>

					{message}
				</Box>
			</Box>

			{isProcessing && <TableLoadingSkeleton />}

			<Divider sx={{ margin: '20px 0px', ml: '44px', mb: '34px' }} light />
		</>
	);
};

export default BotChatMessage;
