import { Box } from '@mui/system';
import { useEffect, useState } from 'react';
import ChatSideBarComponent from '../ChatSidebar';
import ChatMainWindowComponent from '../ChatWindow';
import { ChatMessageData, ChatSessionData } from '../../../types/apis';
import ws, { Socket } from 'socket.io-client';
import moment from 'moment';
import DynamicTableComponent from '../../shared/DynamicTableWithStepsComponent';
import { uniqueNamesGenerator, colors, starWars } from 'unique-names-generator';
import { useStores } from '../../../mobxStore/rootStore';
import _ from 'lodash';
import { v4 as uuidv4 } from 'uuid';
//import { observer } from 'mobx-react-lite';
import { ACCESS_LIST } from '../../../utils/utilFunctions';
import { useNavigate } from 'react-router-dom';
import { toJS } from 'mobx';
import { StepData } from '../../../types/apis/socket';
// import { TEXT_CONSTANTS } from '../../../utils/TextContants';
interface ChatMainComponentProps {}

const ChatMainComponent = ({}: ChatMainComponentProps) => {
	const navigate = useNavigate();
	const { chatStore } = useStores();

	const [chatSessions, setChatSessions] = useState<ChatSessionData[]>([]);
	const [isAdmin] = useState<boolean>(
		localStorage.getItem('user_id') &&
			_.size(localStorage.getItem('user_id')?.split('.')) > 0 &&
			localStorage.getItem('user_id')?.split('.')[1] === 'admin'
			? true
			: false,
	);

	const [userId] = useState<string>(
		localStorage.getItem('user_id') ? localStorage.getItem('user_id')?.split('.')[0] ?? '' : '',
	);
	const [selectedChatSession, setSelectedChatSession] = useState<ChatSessionData>();
	const [socketConnection, setSocketConnection] = useState<Socket>();
	const [message, setMessage] = useState<string>('');
	const [isChatSessionLoading, setChatSessionLoading] = useState<boolean>(true);
	const [isMessageLoading, setIsMessageLoading] = useState<boolean>(true);
	const [isMessageProcessing, setIsMessageProcessing] = useState<null | string>(null);
	const [chats, setChats] = useState<any[]>([]);
	const [tempChats, setTempChats] = useState<any>({});
	const [isChatConnected, setIsChatConnected] = useState<boolean>(false);

	const handleNewSession = async () => {
		try {
			const chat_session_name: string = uniqueNamesGenerator({
				dictionaries: [starWars, colors],
				style: 'lowerCase',
				separator: ' ',
			});
			const data = await chatStore.createNewChatSession({
				//@ts-ignore
				user_id: userId,
				chat_session_name,
				id: uuidv4(),
				created_at: moment().toISOString(),
				modified_at: moment().toISOString(),
				chat: [],
			});

			setChats([]);

			setChatSessions((prev) => {
				if (!Array.isArray(prev)) return [data];
				return [data, ...prev];
			});

			setSelectedChatSession(data);
		} catch (error) {}
	};

	const handleWsConnection = () => {
		console.log("IP:", process.env.REACT_APP_SOCKET_BASE_URL!)
		const socket = ws(
			process.env.REACT_APP_SOCKET_BASE_URL!,
			{
				"transports":  ["websocket"],
			}
		);
		
		setSocketConnection(socket);
	};

	useEffect(() => {
		socketConnection?.on('message', async (data) => {
			try {
				if (data.type === 'INTERMEDIATE') {
					setIsMessageProcessing(data.message);
				}

				if (data.type === 'FINAL') {
					let tempChatMessage = _.cloneDeep(tempChats);

					let tempStepData: StepData = data.step_data;

					let followup: string | undefined;
					let followUpData = _.find(tempStepData, (itm: StepData) => {
						if (
							itm.step_id === 3 &&
							_.has(itm?.data, 'follow_up_question') &&
							_.has(itm?.data, 'answerable') &&
							itm?.data?.answerable === false
						) {
							return true;
						} else {
							return false;
						}
					});
					if (followUpData) {
						followup = followUpData?.data?.follow_up_question;
					}

					if (tempChatMessage) {
						tempChatMessage = {
							...tempChatMessage,
							query_meta_data: data,
							response: 'COMPLETED',
						};

						let tempChatSessionsData: any = _.cloneDeep(chatSessions);
						let index = _.findIndex(tempChatSessionsData, (item: any) => {
							return item?.id === selectedChatSession?.id;
						});
						if (index !== -1) {
							tempChatSessionsData[index].chat.push(tempChatMessage);
							chatStore.updateChatSessions(tempChatSessionsData);

							setChatSessions(tempChatSessionsData);
						}
					}
					setTempChats({});
					setChats((prev) => [
						...prev,
						{
							type: 'bot',
							message: (
								<DynamicTableComponent
									steps={data.step_data}
									data={data?.data}
									query_id={data?.query_id}
									isAdmin={isAdmin}
									followup={followup}
								/>
							),
							query_id: data?.query_id,
						},
					]);
					setIsMessageProcessing(null);
				}
			} catch (error) {
				console.error("Error in socket.on('message'):");
			}
		});

		return () => {
			socketConnection?.removeAllListeners('message');
		};
	});

	const getChatSessions = async () => {
		try {
			const data = await chatStore.fetchAllChatSessions();

			if (!data) {
				return handleNewSession();
			}

			let myTempData = _.cloneDeep(data);
			myTempData.sort((a: ChatSessionData, b: ChatSessionData) => {
				if (moment(a.created_at).isBefore(moment(b.created_at))) {
					return 1;
				} else if (moment(a.created_at).isSame(moment(b.created_at))) {
					return 0;
				} else {
					return -1;
				}
			});

			setChatSessions(myTempData);

			if (moment(myTempData[0].created_at).add(8, 'h').isBefore(moment())) {
				return handleNewSession();
			} else {
				setSelectedChatSession(myTempData[0]);
			}
		} catch (error) {}
	};

	const deleteChatSession = async (session_id: string) => {
		try {
			await chatStore.deleteChatSession(session_id);
			const updatedChatSessions = chatSessions.filter((session) => session.id !== session_id);
			setChatSessions(updatedChatSessions);
			if (_.size(updatedChatSessions) >= 1) {
				setTempChats({});
				processChatData(updatedChatSessions[0].chat);
				setSelectedChatSession(updatedChatSessions[0]);
			} else {
				setTempChats({});
				setChats([]);
				setSelectedChatSession(undefined);
			}
		} catch (error) {}
	};

	const handleSocketEmit = (message: string) => {
		if (!selectedChatSession) return;

		let index = -1;
		let allChatSessions = toJS(chatStore.allChatSessions.data);
		index = _.findIndex(allChatSessions, (item) => item.id === selectedChatSession.id);
		let history: any = [];

		if (index !== -1 && message !== 'CONNECTED' && message !== 'DISCONNECTED') {
			let formatedChatHistory: any = [];
			_.forEach(allChatSessions?.[index].chat, (item: ChatMessageData) => {
				if (_.has(item, 'user_query')) {
					formatedChatHistory.push({ user: item.user_query });
				}

				//@ts-ignore
				let tempStepData: StepData = item?.query_meta_data?.step_data;

				let followup: string | undefined;
				let followUpData = _.find(tempStepData, (itm: StepData) => {
					if (
						itm?.step_id === 3 &&
						_.has(itm?.data, 'follow_up_question') &&
						_.has(itm?.data, 'answerable') &&
						itm?.data?.answerable === false
					) {
						return true;
					} else {
						return false;
					}
				});
				if (followUpData) {
					followup = followUpData?.data?.follow_up_question;
					formatedChatHistory.push({ ai: followup });
				} else if (
					_.has(item, 'query_meta_data') &&
					_.has(item.query_meta_data, 'step_data') &&
					_.findIndex(
						//@ts-ignore
						item.query_meta_data.step_data,
						(itm) =>
							//@ts-ignore
							itm.display_name === 'GenerateQuery',
					) !== -1
				) {
					//@ts-ignore
					let generated_query_temp_response = _.find(
						//@ts-ignore
						item.query_meta_data.step_data,
						(itm) =>
							//@ts-ignore
							itm.display_name === 'GenerateQuery',
					)?.data?.generated_query?.[0]?.response;

					let ai_response = generated_query_temp_response;
					if (ai_response) {
						formatedChatHistory.push({ ai: ai_response });
					}
				}
			});
			history = formatedChatHistory;
		}

		socketConnection?.emit('message', {
			chat_id: selectedChatSession.id,
			chat_session_id: selectedChatSession.id,
			user_id: userId,
			message: message,
			history: history,
		});
	};

	const handleAskQuestions = async (e: any) => {
		e.preventDefault();
		if (!selectedChatSession || !message || isMessageProcessing) return;
		await handleSocketEmit('CONNECTED');
		let tempChatMessage = {
			chat_id: selectedChatSession?.id,
			created_at: moment().toISOString(),
			feedback: null,
			id: uuidv4(),
			query_meta_data: {
				data: {
					data: [],
				},
				type: 'EXECUTING',
			},
			user_query: message,
			response_time: 0,
			response: '',
		};
		setTempChats(tempChatMessage);
		handleSocketEmit(message);

		setChats((prev) => [...prev, { type: 'user', message, created_at: moment() }]);
		setMessage('');
	};

	/* const handleAskQFromSuggestions = async (
		q: any,
		isFromUrl?: boolean | undefined,
		processedChatData?: any,
	) => {
		if (!selectedChatSession || !q || (isFromUrl ? false : isMessageProcessing)) return;

		handleSocketEmit(q);
		setChats([
			...(isFromUrl ? processedChatData : chats),
			{ type: 'user', message: q, created_at: moment() },
		]);
	}; */

	const updateSelectedChatSession = async (chatSession: ChatSessionData) => {
		handleSocketEmit('DISCONNECTED');

		let tempChatSessionsData: any = _.cloneDeep(chatSessions);

		setTempChats({});
		setChats([]);
		setIsMessageLoading(true);

		setTimeout(() => {
			let index = _.findIndex(tempChatSessionsData, (item: any) => {
				return item.id === chatSession?.id;
			});

			if (index !== -1) {
				setSelectedChatSession(tempChatSessionsData?.[index]);
				processChatData(tempChatSessionsData?.[index]?.chat);
			}
		}, 100);
	};

	const handleInitialApiCall = async () => {
		setChatSessionLoading(true);
		await handleWsConnection();
		await getChatSessions();
		setChatSessionLoading(false);
	};

	const handleGetAllChatMessages = async () => {
		setIsMessageLoading(true);
		try {
			let allChatSessions: ChatSessionData[] = toJS(chatStore.allChatSessions.data) ?? [];
			if (_.size(allChatSessions) > 0) {
				allChatSessions.sort((a: ChatSessionData, b: ChatSessionData) => {
					if (moment(a.created_at).isBefore(moment(b.created_at))) {
						return 1;
					} else if (moment(a.created_at).isSame(moment(b.created_at))) {
						return 0;
					} else {
						return -1;
					}
				});
				const data = allChatSessions?.[0]?.chat;

				await processChatData(data);
			}
		} catch (error) {}
		setIsMessageLoading(false);
	};

	const processChatData = async (chatData: any[]) => {
		const processedChats: any[] = [];

		chatData?.forEach((entry) => {
			if (entry?.query_meta_data?.type === 'FINAL') {
				processedChats.push({
					type: 'user',
					message: entry.user_query,
					created_at: entry?.created_at,
				});

				let tempStepData: StepData = entry.step_data;

				let followup: string | undefined;
				let followUpData = _.find(tempStepData, (itm: StepData) => {
					if (
						itm.step_id === 3 &&
						_.has(itm?.data, 'follow_up_question') &&
						_.has(itm?.data, 'answerable') &&
						itm?.data?.answerable === false
					) {
						return true;
					} else {
						return false;
					}
				});
				if (followUpData) {
					followup = followUpData?.data?.follow_up_question;
				}
				processedChats.push({
					type: 'bot',
					query_id: entry?.query_meta_data?.query_id,
					feedback: entry?.feedback,
					message: (
						<DynamicTableComponent
							steps={entry.query_meta_data?.step_data}
							data={entry.query_meta_data.data}
							query_id={entry?.query_meta_data?.query_id}
							isAdmin={isAdmin}
							followup={followup}
						/>
					),
				});
			}
		});

		setIsMessageLoading(false);
		setChats(() => processedChats);
		return processedChats;
	};

	useEffect(() => {
		if (!selectedChatSession) {
			return;
		} else if (isMessageLoading) {
			(async function () {
				await handleSocketEmit('CONNECTED');
				setChats([]);
				setIsMessageProcessing(null);
				handleGetAllChatMessages();
			})();
		}
	}, [selectedChatSession]);

	useEffect(() => {
		handleInitialApiCall();
	}, []);

	useEffect(() => {
		let access_id: string = localStorage.getItem('user_id') ?? '';
		if (!_.some(ACCESS_LIST, (item) => access_id.trim().split('.')[0])) {
			navigate('/');
		}
	});

	return (
		<Box
			sx={{
				position: 'absolute',
				left: 30, //110
				top: '75px',
				display: 'flex',
				height: 'calc(100vh - 75px)',
				width: 'calc(100vw - 30px)',
				overflow: 'hidden',
			}}
		>
			<ChatSideBarComponent
				deleteChatSession={deleteChatSession}
				selectedChatSession={selectedChatSession!}
				setSelectedChatSession={updateSelectedChatSession}
				chatSessions={chatSessions}
				handleNewSession={handleNewSession}
				isChatSessionLoading={isChatSessionLoading}
			/>
			<ChatMainWindowComponent
				chats={chats}
				isMessageProcessing={isMessageProcessing}
				message={message}
				handleAskQuestions={handleAskQuestions}
				setMessage={setMessage}
				selectedChatSession={selectedChatSession}
				//handleAskQFromSuggestions={handleAskQFromSuggestions}
				isMessageLoading={isMessageLoading}
			/>
		</Box>
	);
};

export default ChatMainComponent;
