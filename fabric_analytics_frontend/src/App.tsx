import Routes from './routes/index';
import { useEffect } from 'react';
import Box from '@mui/material/Box';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './index.css';
import { LicenseManager } from '@ag-grid-enterprise/core';
import { v4 as uuidv4 } from 'uuid';
import { useStores } from './mobxStore/rootStore';
import _ from 'lodash';
// import { TEXT_CONSTANTS } from './utils/TextContants';

//@ts-ignore
LicenseManager.setLicenseKey(process.env.REACT_APP_AGGRID_LICENSE);
// LicenseManager.setLicenseKey(TEXT_CONSTANTS.REACT_APP_AGGRID_LICENSE);

function App() {
	const { chatStore } = useStores();

	useEffect(() => {
		if (_.size(JSON.parse(localStorage.getItem('chatSessions') ?? 'null')) > 0) {
			let tempChatSessions = JSON.parse(localStorage.getItem('chatSessions') ?? 'null');

			chatStore.updateChatSessions(tempChatSessions);
		}
	}, []);

	useEffect(() => {
		window.onbeforeunload = function handleUnload() {
			chatStore.saveToLocalStorage();
		};
		return () => {
			window.onbeforeunload = null;
		};
	}, []);

	return (
		<Box>
			<Routes />
			<ToastContainer
				position="top-right"
				autoClose={1300}
				hideProgressBar
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss
				draggable
				pauseOnHover
				theme="colored"
			/>
		</Box>
	);
}

export default App;
