import { Box, Skeleton } from '@mui/material';
import React from 'react';

const TableLoadingSkeleton = () => {
	return (
		<Box sx={{ backgroundColor: 'transparent' }}>
			<Box sx={{ width: '100%', margin: '10px 15px' }}>
				<Box
					sx={{
						width: '100%',
						display: 'flex',
						alignItems: 'center',
						marginBottom: '10px',
					}}
				>
					<Skeleton
						height="30px"
						width="30px"
						sx={{ borderRadius: '5px' }}
						variant="rounded"
					/>
					<Skeleton
						height="15px"
						width="10%"
						sx={{ borderRadius: '5px', marginLeft: '10px' }}
						variant="rectangular"
					/>
				</Box>
				<Skeleton
					height="30px"
					width="100%"
					sx={{ borderRadius: '5px' }}
					variant="rectangular"
				/>
			</Box>
			<Box sx={{ padding: '15px' }}>
				{[34, 5, 3, 5, 3].map((el, index) => {
					return (
						<Box display="flex" mt="40px" justifyContent="space-between" key={index}>
							<Skeleton variant="rounded" width={'25%'} height={20} />
							<Skeleton variant="rounded" width={'15%'} height={20} />
							<Skeleton variant="rounded" width={'15%'} height={20} />
						</Box>
					);
				})}
			</Box>
		</Box>
	);
};

export default TableLoadingSkeleton;
