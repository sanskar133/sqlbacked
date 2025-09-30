import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import Tooltip, { TooltipProps, tooltipClasses } from '@mui/material/Tooltip';
import parse from 'html-react-parser';

/* Custom tool tip renderer function. It renders title and description of a Tile chart */
export const renderCustomTooltipTile = (title: string, desc: string) => {
	return (
		<div className="custom-chart-tooltip">
			<div className="custom-chart-tooltip-container">
				<span
					className="custom-chart-tooltip-category"
					style={{
						alignItems: 'flex-start !important',

						borderBottom: '1px solid rgba(255,255,255,0.4)',
						width: '100%',
					}}
				>
					{title}
				</span>

				<Stack
					width="100%"
					direction="row"
					gap="8px"
					alignItems="flex-start"
					justifyContent="space-between"
				>
					<span className="custom-chart-tooltip-title" style={{ textAlign: 'start' }}>
						{/* If there is html in the string then show parse html and create html elements */}
						{parse(desc)}
					</span>
				</Stack>
			</div>
		</div>
	);
};

/* Tooltip customization to show black background and black arrow */
export const BootstrapTooltip = styled(({ className, ...props }: TooltipProps) => (
	<Tooltip {...props} arrow classes={{ popper: className }} />
))(({ theme }) => ({
	[`& .${tooltipClasses.arrow}`]: {
		color: theme.palette.common.black,
	},
	[`& .${tooltipClasses.tooltip}`]: {
		backgroundColor: theme.palette.common.black,
	},
}));
