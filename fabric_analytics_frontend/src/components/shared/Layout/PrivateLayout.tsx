import { ChildrenProps } from '../../../types/types';
import HeaderComponent from './Header';
import { Box } from '@mui/material';

const PrivateLayout = ({ children }: ChildrenProps) => {
	return (
		<Box>
			<HeaderComponent />
			<Box sx={{ padding: '12px 30px 12px 30px' }}>{children}</Box>
		</Box>
	);
};

export default PrivateLayout;
