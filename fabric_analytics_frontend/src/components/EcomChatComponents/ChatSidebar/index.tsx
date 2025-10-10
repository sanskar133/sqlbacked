import { Box, Typography, Button } from '@mui/material';
import { useEffect, useState } from 'react';
import { SvgPlusIcon } from '../../shared/AppIcons';
import { theme } from '../../../theme';
import { ChatSessionData } from '../../../types/apis';
import ChatSessionListComponent from './ChatSessionListComponent';
import ChatSessionLoadingSkeleton from './ChatSessionLoadingSkeleton';

interface ChatSideBarComponentProps {
	handleNewSession: () => void;
	chatSessions: ChatSessionData[];
	setSelectedChatSession: (data: ChatSessionData) => void;
	selectedChatSession: ChatSessionData;
	deleteChatSession: (id: string) => void;
	isChatSessionLoading: boolean;
}

const ChatSideBarComponent = ({
	handleNewSession,
	deleteChatSession,
	chatSessions,
	setSelectedChatSession,
	isChatSessionLoading,
	selectedChatSession,
}: ChatSideBarComponentProps) => {
	const renderChatSessions = (
		title: string,
		filterFunction: (session: ChatSessionData) => boolean,
	) => {};

	return (
		<Box
			sx={{
				maxWidth: '209px',
				minWidth: '150px',
				display: 'flex',
				position: 'absolute',
				top: '10px',
				left: '10px',
				alignItems: 'center',
				justifyContent: 'space-between',
				padding: '10px 14px',
				borderBottom: '1px solid',
				zIndex: 1,
				borderColor: theme.palette.grey.A100,
			}}
		>
			<Typography variant="body1" fontWeight="600">
				New Chat
			</Typography>
			<Button
				variant="contained"
				sx={{ padding: '6px', borderRadius: '8px', minWidth: 'auto' }}
				onClick={handleNewSession}
			>
				<SvgPlusIcon />
			</Button>
		</Box>
	);
};

export default ChatSideBarComponent;
