import { action, makeObservable, observable, runInAction, toJS } from 'mobx';
import { ChatSessionStoreType } from '../types/apis/mobx';
import _ from 'lodash';
import { ChatSessionData } from '../types/apis';

const initialAllChatSessions: ChatSessionStoreType = {
	data: null,
	error: null,
	isFirstLoading: true,
	isLoading: true,
};

export class ChatStore {
	allChatSessions: ChatSessionStoreType = initialAllChatSessions;
	rootStore: any;

	constructor(rootStore: any) {
		makeObservable(this, {
			allChatSessions: observable,
			fetchAllChatSessions: action,
			updateChatSessions: action,
			forceFetchAllChatSessions: action,
			saveToLocalStorage: action,
		});
		this.rootStore = rootStore;
	}

	fetchAllChatSessions = async () => {
		try {
			runInAction(() => {
				this.allChatSessions.isLoading = true;
			});

			runInAction(() => {
				this.allChatSessions.error = null;
				this.allChatSessions.isLoading = false;

				if (this.allChatSessions.isFirstLoading === true) {
					this.allChatSessions.isFirstLoading = false;
				}
			});

			return toJS(this.allChatSessions.data);
		} catch (error) {
			runInAction(() => {
				this.allChatSessions.isLoading = false;
				this.allChatSessions.error = error as string;
			});

			throw error;
		}
	};

	forceFetchAllChatSessions = async (database_connection_id: string) => {
		this.allChatSessions.isLoading = true;
		try {
			runInAction(() => {
				this.allChatSessions.error = null;
				this.allChatSessions.isLoading = false;

				if (this.allChatSessions.isFirstLoading === true) {
					this.allChatSessions.isFirstLoading = false;
				}
			});

			return toJS(this.allChatSessions.data);
		} catch (error) {
			runInAction(() => {
				this.allChatSessions.isLoading = false;
				this.allChatSessions.error = error as string;
			});

			throw error;
		}
	};

	createNewChatSession = async (payload: ChatSessionData) => {
		try {
			runInAction(() => {
				if (_.size(this.allChatSessions.data) === 0) {
					this.allChatSessions.data = [payload];
				} else {
					let tempData = [...(this.allChatSessions.data ?? []), ...[payload]];

					this.allChatSessions.data = tempData;
				}
			});
			return payload;
		} catch (error) {
			throw error;
		}
	};

	updateChatSessions = async (payload: any) => {
		try {
			runInAction(() => {
				this.allChatSessions.data = payload;
			});
			return payload;
		} catch (error) {
			throw error;
		}
	};

	saveToLocalStorage = () => {
		try {
			if (_.size(this.allChatSessions.data) > 0) {
				localStorage.setItem('chatSessions', JSON.stringify(this.allChatSessions.data));
			} else {
				localStorage.setItem('chatSessions', JSON.stringify(null));
			}
		} catch (e) {}
	};

	deleteChatSession = async (id: string) => {
		try {
			runInAction(() => {
				this.allChatSessions.data = _.filter(
					this.allChatSessions.data,
					(item) => item.id !== id,
				);

				if (_.size(this.allChatSessions.data) === 0) {
					this.allChatSessions.data = null;
				}
			});
			return true;
		} catch (error) {
			throw error;
		}
	};
}

export default ChatStore;
