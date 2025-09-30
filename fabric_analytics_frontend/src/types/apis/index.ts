export interface ChatSessionData {
	id: string;
	user_id: string;
	chat_session_name: string;
	created_at: string;
	modified_at: string;
	chat: ChatMessageData[];
}

export interface SocketChatMessageData {
	chat_id: string;
	message: string;
	status_code: number;
	error_message: any;
	data: {
		data: any;
	};
	type: string;
}
export interface ChatMessageData {
	id: string;
	chat_id: string;
	user_query: string;
	query_meta_data: SocketChatMessageData;
	response: string;
	response_time: string;
	created_at: string;
}
