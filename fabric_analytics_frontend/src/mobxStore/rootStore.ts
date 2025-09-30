import React from 'react';

import ChatStore from './chatStore';

export class RootStore {
	chatStore: ChatStore;

	constructor() {
		this.chatStore = new ChatStore(this);
	}
}

const StoresContext = React.createContext(new RootStore());

// this will be the function available for the app to connect to the stores
export const useStores = () => React.useContext(StoresContext);
