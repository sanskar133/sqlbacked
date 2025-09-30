export interface StepData {
	display_name: string;
	error_message: string;
	message: string;
	step_id: number;
	data: any;
}

export interface SocketResponseData {
	chat_id: string;
	error_message: string;
	message: string;
	status_code: number;
	type: string;
	data: any;
	query_id: string;
	step_data: any[];
}
