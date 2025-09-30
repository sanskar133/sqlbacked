import { Box, OutlinedInput, InputAdornment } from '@mui/material';
import React, { useEffect, useRef } from 'react';
import { ChatSendIcon } from '../../shared/AppIcons';
import UserChatMessage from './UserChatMessage';
import BotChatMessage from './BotChatMessage';
import { ChatSessionData } from '../../../types/apis';
import ChatMessageLoaderSkeleton from './ChatMessageLoaderSkeleton';
interface ChatMainWindowComponentPropse {
	setMessage: (data: any) => void;
	handleAskQuestions: (e: any) => void;
	message: string;
	isMessageProcessing: string | null;
	chats: any[];
	isSharePage?: boolean;
	selectedChatSession?: ChatSessionData;
	//handleAskQFromSuggestions?: (data: any) => void;
	isMessageLoading: boolean;
}

const ChatMainWindowComponent = ({
	setMessage,
	handleAskQuestions,
	message,
	isMessageProcessing,
	chats,
	isSharePage = false,
	selectedChatSession,
	//handleAskQFromSuggestions,
	isMessageLoading,
}: ChatMainWindowComponentPropse) => {
	const messagesEndRef = useRef<HTMLDivElement | null>(null);
	const scrollToBottom = () => {
		if (messagesEndRef.current) {
			messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
		}
	};

	useEffect(() => {
		if (isMessageProcessing === null) {
			setTimeout(() => {
				scrollToBottom();
			}, 1000);
		}
	}, [chats, isMessageProcessing]);

	/* const handleSubmitSuggestion = (q: any) => {
		if (handleAskQFromSuggestions) handleAskQFromSuggestions(q);
	};
 */
	return (
		<>
			<Box
				sx={{
					display: 'flex',
					flexDirection: 'column',
					height: '100',
					width: isSharePage ? '100vw' : 'calc(100vw - 279px)',
					marginLeft: !isSharePage ? '10px' : '0',
					position: 'relative',
				}}
			>
				<Box
					sx={{
						padding: '20px 15%',
						overflowY: 'scroll',
						position: 'relative',
						height: '100%',
						marginBottom: isSharePage ? '0px' : '100px',
					}}
					className="string-background fab-hide-scrollbar"
				>
					{isMessageLoading ? (
						<ChatMessageLoaderSkeleton />
					) : (
						<Box>
							{chats?.map(
								(
									el: {
										message: string;
										type: string;
										query_id: string;
										feedback: boolean | null | undefined;
										created_at?: undefined | string;
									},
									key,
								) => {
									if (el.type === 'user')
										return (
											<React.Fragment key={key}>
												<UserChatMessage
													message={el.message}
													created_at={el?.created_at}
												/>
											</React.Fragment>
										);

									if (el.type === 'bot')
										return (
											<React.Fragment key={key}>
												<BotChatMessage
													isProcessing={false}
													message={el.message}
												/>
											</React.Fragment>
										);

									return <></>;
								},
							)}
							{isMessageProcessing && (
								<>
									<BotChatMessage
										isProcessing={true}
										processingMessage={isMessageProcessing}
										message={''}
									/>
								</>
							)}
						</Box>
					)}

					<Box mb="50px" ref={messagesEndRef} />
				</Box>
				{/* {size(chats) === 0 && isSharePage === false && !isMessageLoading && (
					<Box
						sx={{
							position: 'absolute',
							bottom: '50px',
							width: '100%',
							padding: '20px 15%',
							// transform: 'translate(0%, -50%)',
						}}
					>
						<Grid container spacing={1} sx={{ paddingBlock: '30px' }}>
							{map(selectedConnection?.sample_questions, (question, index) => (
								<Grid
									item
									xs={6}
									onClick={(e) => handleSubmitSuggestion(question)}
									key={index}
								>
									<Box
										sx={{
											display: 'flex',
											flex: 1,
											height: '100%',
											border: '1px solid #E4E7EC',
											borderRadius: '8px',
											padding: '10px 12px',
											cursor: 'pointer',
											background: 'transparent',
											color: '#5E5468',
											':hover': {
												background: '#F1F3F5',
												color: '#101828',
												'& .straight-icon': {
													// Use a class to target the StraightIcon
													visibility: 'visible',
												},
											},
										}}
										className="chat-page-bulb-icon-crtl"
									>
										<BulbIcon
											sx={{
												fontSize: '16px',
												color: 'transparent',
											}}
											className="chat-page-bulb-icon"
										/>
										<Typography
											sx={{
												color: 'inherit',
												fontSize: '14px',
												fontWeight: 400,
												lineHeight: '20px',
												marginLeft: '8px',
												width: '80%',
											}}
										>
											{question}
										</Typography>
										<ArrowIcon
											className="straight-icon"
											sx={{
												color: 'inherit',
												marginLeft: '10px',
												visibility: 'hidden',
												fontSize: '20px',
											}}
										/>
									</Box>
								</Grid>
							))}
						</Grid>
					</Box>
				)} */}
				{isSharePage === true ? null : (
					<Box
						sx={{
							position: 'absolute',
							bottom: '0px',
							width: '100%',
							padding: '20px 15%',
						}}
					>
						<form
							onSubmit={handleAskQuestions}
							style={{
								boxShadow: '0px 4px 7px 0px rgba(208, 213, 221, 0.30)',
								borderRadius: '8px',
							}}
						>
							<OutlinedInput
								sx={{
									width: '100%',
									border: 'none !important',
									'& .MuiOutlinedInput-notchedOutline': {
										borderColor: 'transparent',
									},
								}}
								autoComplete="off"
								id="outlined-adornment-weight"
								endAdornment={
									<InputAdornment position="end" onClick={handleAskQuestions}>
										<Box
											sx={{
												minWidth: '28px',
												minHeight: '28px',
												borderRadius: '4px',
												display: 'flex',
												alignItems: 'center',
												justifyContent: 'center',
												cursor: message === '' ? 'not-allowed' : 'pointer',
												background:
													message === ''
														? 'rgba(251, 98, 56, 0.7)'
														: '#FB6238',
											}}
										>
											<ChatSendIcon />
										</Box>
									</InputAdornment>
								}
								aria-describedby="outlined-weight-helper-text"
								inputProps={{
									'aria-label': 'weight',
								}}
								value={message}
								onChange={(e) => {
									setMessage(e.target.value);
								}}
							/>
						</form>
					</Box>
				)}
			</Box>
		</>
	);
};

export default ChatMainWindowComponent;
