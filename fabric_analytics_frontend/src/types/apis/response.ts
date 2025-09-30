import { ChatSessionData } from '.';

export interface responseStructure {
	code: boolean;
	message: string;
	statusCode: number;
}

export interface GetAllChatSessionsApiResponse extends responseStructure {
	result: ChatSessionData[];
}
