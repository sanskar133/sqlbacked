import { ChatSessionData, ChatMessageData } from '.';

export interface mobxBase {
	error: string | null;
	isFirstLoading: boolean;
	isLoading: boolean;
}

export interface ChatSessionStoreType extends mobxBase {
	data: ChatSessionData[] | null;
}

export interface ChatMessageStoreType extends mobxBase {
	data: ChatMessageData[] | null;
}

export interface ChatMessageStoreType extends mobxBase {
	data: ChatMessageData[] | null;
}
