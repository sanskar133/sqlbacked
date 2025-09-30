import { Skeleton /* Typography */ } from '@mui/material';
import { Box } from '@mui/system';
import { map } from 'lodash';
import React from 'react';
import TableLoadingSkeleton from '../../../shared/TableLoadingSkeleton/TableLoadingSkeleton';

const ChatMessageLoaderSkeleton = () => {
	return (
		<Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', flexWrap: 'wrap' }}>
			{map(Array(1).fill(4), (value, index) => (
				<Box sx={{ width: '100%', margin: '10px 15px' }} key={index}>
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
			))}
			<Box sx={{ marginTop: '50px' }}>
				<TableLoadingSkeleton />
			</Box>
		</Box>
	);
};

export default ChatMessageLoaderSkeleton;
