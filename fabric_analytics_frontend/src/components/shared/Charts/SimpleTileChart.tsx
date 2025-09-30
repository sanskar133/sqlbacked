import { Stack, Typography } from '@mui/material';
import { useEffect, useRef, useState } from 'react';
import { formatTileNumber } from '../../../utils/utilFunctions';

interface SimpleTileChartProps {
	title: string;
	value: number | string;
}

function SimpleTileChart({ title, value }: SimpleTileChartProps) {
	const containerRef = useRef<HTMLDivElement | null>(null);

	const [isOverflowing, setIsOverflowing] = useState(false);

	useEffect(() => {
		const checkOverflow = () => {
			if (containerRef.current) {
				const hasOverflow =
					containerRef.current.scrollHeight > containerRef.current.offsetHeight;
				setIsOverflowing(hasOverflow);
			}
		};

		// Initial check
		checkOverflow();

		// Check overflow on window resize
		window.addEventListener('resize', checkOverflow);

		// Cleanup event listener on unmount
		return () => {
			window.removeEventListener('resize', checkOverflow);
		};
	}, []);

	return (
		<Stack
			width="100%"
			height="300px"
			sx={{
				backgroundColor: 'rgba(255, 255, 255, 0.4)',
				borderRadius: '8px',
			}}
		>
			<Stack
				direction="row"
				sx={{
					borderBottom: '1px solid rgba(0, 0, 0, 0.08)',
					padding: '16px 15px',
					alignItems: 'center',
				}}
			>
				<Typography
					variant="customPrmH4"
					sx={{ textTransform: 'uppercase', color: '#5E5468' }}
				>
					{title !== undefined || title !== null
						? title?.replaceAll('_', ' ') ?? 'None'
						: 'None'}
				</Typography>
			</Stack>
			<Stack
				width="100%"
				height="calc(100% - 62.89px)"
				alignItems="center"
				justifyContent={isOverflowing ? 'flex-start' : 'center'}
				sx={{ padding: '16px 15px', overflowY: 'auto' }}
				ref={containerRef}
			>
				<Typography variant="h3">
					{typeof value === 'string' ? (
						value
					) : (
						<>{!isNaN(value) ? formatTileNumber(value, title) : value}</>
					)}
				</Typography>
			</Stack>
		</Stack>
	);
}

export default SimpleTileChart;
