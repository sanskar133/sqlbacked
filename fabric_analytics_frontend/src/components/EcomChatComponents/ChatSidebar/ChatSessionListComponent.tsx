import {
	IconButton,
	List,
	ListItem,
	MenuItem,
	Tooltip,
	TooltipProps,
	Typography,
} from '@mui/material';
import { ChatSessionData } from '../../../types/apis';
import { Box } from '@mui/system';
import { styled } from '@mui/material/styles';
import { tooltipClasses } from '@mui/material/Tooltip';
import { SvgTrashBinIcon } from '../../shared/AppIcons';
import { GridMoreVertIcon } from '@mui/x-data-grid';

interface ChatSessionListComponentProps {
	setSelectedChatSession: (el: any) => void;
	selectedChatSession: any;
	chatSessions: ChatSessionData[];
	deleteChatSession: (id: string) => void;
}

const LightTooltip = styled(({ className, ...props }: TooltipProps) => (
	<Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
	[`& .${tooltipClasses.tooltip}`]: {
		backgroundColor: theme.palette.common.white,
		color: 'rgba(0, 0, 0, 0.87)',
		boxShadow: theme.shadows[1],
		fontSize: 11,
		paddingInline: '0px',
	},
}));

const ChatSessionListComponent = ({
	chatSessions,
	deleteChatSession,
	setSelectedChatSession,
	selectedChatSession,
}: ChatSessionListComponentProps) => {
	return (
		<List sx={{ width: '100%', paddingBottom: '10px' }}>
			{chatSessions?.map((el: ChatSessionData) => {
				return (
					<ListItem
						key={el.id}
						sx={{
							cursor: 'pointer',
							padding: '7px 15px',
							display: 'flex',
							justifyContent: 'space-between',
							borderRadius: '8px',
							alignItems: 'center',
							marginBottom: '15px',
							borderBottom: '1px solid #FFF',
							borderRight: '1px solid #FFF',
							background: `${
								el?.id === selectedChatSession?.id ? '#F2E8F1' : 'transparent'
							}`,

							'&:hover': {
								boxShadow:
									'1.751px 5.252px 19.451px -2.529px rgba(22, 52, 80, 0.10)',
								background: `${
									el?.id === selectedChatSession?.id
										? '#F2E8F1'
										: 'rgba(255, 255, 255, 0.15)'
								}`,
							},
						}}
						onClick={() => {
							setSelectedChatSession(el);
						}}
					>
						<Typography variant="subtitle2" noWrap>
							{el.chat_session_name}
						</Typography>
						<LightTooltip
							sx={{
								paddingInline: '0px',
							}}
							title={
								<Box
									sx={{
										display: 'flex',
										flexDirection: 'column',
										alignItems: 'center',
									}}
								>
									<Box
										sx={{
											display: 'flex',
											alignItems: 'center',
											justifyContent: 'flex-start',
											padding: '0px 10px',
											gap: '16px',
											width: '120px',
											cursor: 'pointer',
											'&:hover': {
												backgroundColor: '#F2E8F9',
											},
										}}
										onMouseDown={() => {
											deleteChatSession(el.id);
										}}
									>
										<MenuItem
											disableGutters
											sx={{
												justifyContent: 'flex-start',
												width: '100%',
												gap: '8px',
											}}
										>
											<SvgTrashBinIcon />
											Delete
										</MenuItem>
									</Box>
								</Box>
							}
						>
							<IconButton size="small">
								<GridMoreVertIcon fontSize="small" />
							</IconButton>
						</LightTooltip>
					</ListItem>
				);
			})}
		</List>
	);
};

export default ChatSessionListComponent;
