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
	) => {
		const filteredChatSessions = chatSessions?.filter(filterFunction) ?? [];

		return (
			<Box width="100%">
				<Typography variant="caption">{title}</Typography>
				{isChatSessionLoading ? (
					<ChatSessionLoadingSkeleton />
				) : (
					<>
						{filteredChatSessions.length === 0 ? (
							<Typography
								sx={{
									backgroundColor: 'rgba(0, 0, 0, 0.05)',
									padding: '11px 10px',
									display: 'flex',
									width: '100%',
									borderRadius: '8px',
									marginBottom: '20px',
								}}
								variant="caption"
								mt="10px"
							>
								No Chats
							</Typography>
						) : (
							<ChatSessionListComponent
								setSelectedChatSession={setSelectedChatSession}
								selectedChatSession={selectedChatSession}
								chatSessions={filteredChatSessions}
								deleteChatSession={deleteChatSession}
							/>
						)}
					</>
				)}
			</Box>
		);
	};

	const isToday = (date: Date) => {
		const today = new Date();
		return (
			date.getDate() === today.getDate() &&
			date.getMonth() === today.getMonth() &&
			date.getFullYear() === today.getFullYear()
		);
	};

	const isYesterday = (date: Date) => {
		const yesterday = new Date();
		yesterday.setDate(yesterday.getDate() - 1);
		return (
			date.getDate() === yesterday.getDate() &&
			date.getMonth() === yesterday.getMonth() &&
			date.getFullYear() === yesterday.getFullYear()
		);
	};

	const isLastSevenDays = (date: Date) => {
		const sevenDaysAgo = new Date();
		sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
		return date >= sevenDaysAgo;
	};

	return (
		<Box
			sx={{
				maxWidth: '209px',
				minWidth: '209px',
				position: 'relative',
				border: '1px solid #FFF',
				borderColor: theme.palette.grey.A100,
				borderRadius: '8px',
				height: 'calc(100vh - 87px)',
				backgroundColor: 'rgba(255,255,255,0.4)',
			}}
		>
			<Box
				sx={{
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'space-between',
					padding: '10px 14px',
					borderBottom: '1px solid',
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
			<Box
				sx={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'start',
					padding: '10px 14px',
					marginTop: '15px',
					height: '75vh',
					overflowY: 'auto',
				}}
				className="fab-hide-scrollbar"
			>
				{renderChatSessions('Today', (session) => isToday(new Date(session.created_at)))}
				{renderChatSessions('Yesterday', (session) =>
					isYesterday(new Date(session.created_at)),
				)}
				{renderChatSessions(
					'Last 7 days',
					(session) =>
						isLastSevenDays(new Date(session.created_at)) &&
						!isToday(new Date(session.created_at)) &&
						!isYesterday(new Date(session.created_at)),
				)}
				{renderChatSessions(
					'Old messages',
					(session) =>
						!isToday(new Date(session.created_at)) &&
						!isYesterday(new Date(session.created_at)) &&
						!isLastSevenDays(new Date(session.created_at)),
				)}
			</Box>
		</Box>
	);
};

export default ChatSideBarComponent;
