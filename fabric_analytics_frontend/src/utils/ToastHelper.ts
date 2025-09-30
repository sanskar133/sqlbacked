import { toast } from 'react-toastify';

export const createErrorMessage = (message: string) => {
	toast.error(message);
};

export const createSuccessMessage = (message: string) => {
	toast(message, {
		style: {
			color: '#2F9E44',
			backgroundColor: '#F6FEF9',
		},
	});
};

export const createToastMessage = (code: number, message: string) => {
	if (code == 401) return createErrorMessage(message);
	createSuccessMessage(message);
};
