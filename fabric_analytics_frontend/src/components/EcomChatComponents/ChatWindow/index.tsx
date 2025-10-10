import { Box, OutlinedInput, InputAdornment } from '@mui/material';
import React, { useEffect, useRef, useState } from 'react';
import { ChatSendIcon } from '../../shared/AppIcons';
import UserChatMessage from './UserChatMessage';
import BotChatMessage from './BotChatMessage';
import { ChatSessionData } from '../../../types/apis';
import ChatMessageLoaderSkeleton from './ChatMessageLoaderSkeleton';
import { motion, AnimatePresence } from 'framer-motion';

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
	newChatKey?: number;
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
	newChatKey,
}: ChatMainWindowComponentPropse) => {
	const messagesEndRef = useRef<HTMLDivElement | null>(null);
	const [isInputCentered, setIsInputCentered] = useState(() => {
		// Always reset to true when newChatKey changes (new chat session)
		if (newChatKey !== undefined) {
			return true;
		}
		// Check if input was previously centered by checking sessionStorage
		const savedState = sessionStorage.getItem('chatInputCentered');
		return savedState !== null ? JSON.parse(savedState) : true;
	});

	const scrollToBottom = () => {
		if (messagesEndRef.current) {
			messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
		}
	};

	// Save input centering state to sessionStorage whenever it changes
	useEffect(() => {
		sessionStorage.setItem('chatInputCentered', JSON.stringify(isInputCentered));
	}, [isInputCentered]);

	// Reset input centering when new chat is created
	useEffect(() => {
		if (chats && chats.length > 0) {
			setIsInputCentered(false);
		} else if (newChatKey !== undefined) {
			setIsInputCentered(true);
		}
	}, [chats, newChatKey]);

	useEffect(() => {
		if (isMessageProcessing === null) {
			setTimeout(() => {
				scrollToBottom();
			}, 1000);
		}
	}, [chats, isMessageProcessing]);

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
					<AnimatePresence mode="wait">
						{isMessageLoading ? (
							<motion.div
								key="skeleton"
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								exit={{ opacity: 0, y: -20 }}
								transition={{ duration: 0.3, ease: 'easeOut' }}
							>
								<ChatMessageLoaderSkeleton />
							</motion.div>
						) : (
							<motion.div
								key="messages"
								initial={{ opacity: 0 }}
								animate={{ opacity: 1 }}
								exit={{ opacity: 0 }}
								transition={{ duration: 0.3 }}
							>
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
									) => (
										<motion.div
											key={key}
											initial={{ opacity: 0, y: 10 }}
											animate={{ opacity: 1, y: 0 }}
											transition={{
												duration: 0.3,
												delay: key * 0.05,
												ease: 'easeOut',
											}}
										>
											{el.type === 'user' ? (
												<UserChatMessage
													message={el.message}
													created_at={el?.created_at}
												/>
											) : (
												<BotChatMessage
													isProcessing={false}
													message={el.message}
												/>
											)}
										</motion.div>
									),
								)}
								{isMessageProcessing && (
									<motion.div
										initial={{ opacity: 0, y: 10 }}
										animate={{ opacity: 1, y: 0 }}
										transition={{ duration: 0.3, ease: 'easeOut' }}
									>
										<BotChatMessage
											isProcessing={true}
											processingMessage={isMessageProcessing}
											message={''}
										/>
									</motion.div>
								)}
							</motion.div>
						)}
					</AnimatePresence>

					<Box mb="50px" ref={messagesEndRef} />
				</Box>
				{isSharePage === true ? null : (
					<AnimatePresence>
						<motion.div
							key={isInputCentered ? 'centered' : 'bottom'}
							initial={{ opacity: 0, y: isInputCentered ? 20 : -20 }}
							animate={{
								opacity: 1,
								y: 0,
								bottom: isInputCentered ? '50%' : '0px',
								transform: isInputCentered ? 'translateY(50%)' : 'translateY(0%)',
							}}
							exit={{ opacity: 0, y: isInputCentered ? 20 : -20 }}
							transition={{
								duration: 0.3,
								ease: 'easeInOut',
								type: 'spring',
								stiffness: 100,
								damping: 15,
							}}
							style={{
								position: 'absolute',
								width: '100%',
								padding: '20px 15%',
							}}
						>
							<Box
								component="form"
								onSubmit={(e) => {
									setIsInputCentered(false);
									handleAskQuestions(e);
								}}
								sx={{
									display: 'flex',
									alignItems: 'center',
									gap: 2,
									backgroundColor: '#ffffff',
									borderRadius: '16px',
									padding: '12px 20px',
									boxShadow:
										'0 4px 20px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.06)',
									border: '1px solid rgba(0, 0, 0, 0.08)',
									transition: 'all 0.2s ease-in-out',
									'&:hover': {
										boxShadow:
											'0 6px 25px rgba(0, 0, 0, 0.12), 0 3px 12px rgba(0, 0, 0, 0.08)',
										transform: 'translateY(-1px)',
									},
									'&:focus-within': {
										boxShadow:
											'0 8px 30px rgba(0, 0, 0, 0.15), 0 4px 15px rgba(0, 0, 0, 0.10)',
										borderColor: 'rgba(251, 98, 56, 0.3)',
										transform: 'translateY(-1px)',
									},
								}}
							>
								<OutlinedInput
									placeholder="Type your message here..."
									sx={{
										flex: 1,
										'& .MuiOutlinedInput-root': {
											'& fieldset': {
												border: 'none',
											},
											'&:hover fieldset': {
												border: 'none',
											},
											'&.Mui-focused fieldset': {
												border: 'none',
											},
											'& input': {
												padding: '12px 0',
												fontSize: '16px',
												lineHeight: 1.5,
												color: '#1a1a1a',
												'&::placeholder': {
													color: '#8B8B8B',
													opacity: 0.8,
												},
											},
										},
									}}
									autoComplete="off"
									value={message}
									onChange={(e) => {
										setMessage(e.target.value);
									}}
								/>
								<Box
									component="button"
									type="submit"
									disabled={message === '' || isMessageProcessing !== null}
									sx={{
										minWidth: '44px',
										minHeight: '44px',
										borderRadius: '12px',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
										cursor:
											message === '' || isMessageProcessing !== null
												? 'not-allowed'
												: 'pointer',
										background:
											message === '' || isMessageProcessing !== null
												? 'linear-gradient(135deg, #E0E0E0 0%, #CCCCCC 100%)'
												: 'linear-gradient(135deg, #FB6238 0%, #E55A2B 100%)',
										transition: 'all 0.2s ease-in-out',
										border: 'none',
										outline: 'none',
										boxShadow:
											message === '' || isMessageProcessing !== null
												? 'none'
												: '0 2px 8px rgba(251, 98, 56, 0.3)',
										'&:hover':
											message !== '' && isMessageProcessing === null
												? {
														transform: 'scale(1.05)',
														boxShadow:
															'0 4px 12px rgba(251, 98, 56, 0.4)',
														background:
															'linear-gradient(135deg, #E55A2B 0%, #D44A1F 100%)',
													}
												: {},
										'&:active':
											message !== '' && isMessageProcessing === null
												? {
														transform: 'scale(0.98)',
													}
												: {},
									}}
								>
									<ChatSendIcon />
								</Box>
							</Box>
						</motion.div>
					</AnimatePresence>
				)}
			</Box>
		</>
	);
};

export default ChatMainWindowComponent;
