import Fade from '@mui/material/Fade';
import Tooltip from '@mui/material/Tooltip';
const CustomToolTip = ({ children, ...rest }: any) => {
	return (
		<Tooltip
			TransitionComponent={Fade}
			TransitionProps={{ timeout: 300 }}
			arrow
			placement="top"
			PopperProps={{
				modifiers: [
					{
						name: 'offset',
						options: {
							offset: [-6, -8],
						},
					},
				],
			}}
			{...rest}
		>
			{children}
		</Tooltip>
	);
};

export default CustomToolTip;
