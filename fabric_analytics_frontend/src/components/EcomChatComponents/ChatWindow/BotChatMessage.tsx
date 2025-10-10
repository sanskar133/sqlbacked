import { Box } from '@mui/system';
import { SvgChatBotSideIcon } from '../../shared/AppIcons';
import {
	CircularProgress,
	Divider,
	Typography,
	Select,
	MenuItem,
	FormControl,
} from '@mui/material';
import TableLoadingSkeleton from '../../shared/TableLoadingSkeleton/TableLoadingSkeleton';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import { useState } from 'react';
import AgChartComponent from '../../shared/AgChartComponent';

const BotChatMessage = ({
	message,
	isProcessing,
	processingMessage,
}: {
	message: any;
	isProcessing: boolean;
	processingMessage?: string;
}) => {
	console.log('Vis-mess', message);
	const [selectedSection, setSelectedSection] = useState('analysis');

	const sectionOptions = [
		{ value: 'analysis', label: '📝 Response Analysis', icon: '📝' },
		{ value: 'sql', label: '🔍 SQL Query', icon: '🔍' },
		{ value: 'table', label: '📊 Data Table', icon: '📊' },
		{ value: 'plots', label: '📈 Data Plots', icon: '📈' },
	];

	const renderSectionContent = () => {
		switch (selectedSection) {
			case 'sql':
				return responseData.sqlQuery ? (
					<Box sx={{ p: 0 }}>
						<SyntaxHighlighter
							language="sql"
							style={tomorrow}
							customStyle={{ margin: 0, borderRadius: 0, fontSize: '14px' }}
						>
							{responseData.sqlQuery}
						</SyntaxHighlighter>
					</Box>
				) : (
					<Box sx={{ p: 2, textAlign: 'center' }}>
						<Typography color="text.secondary">No SQL query available</Typography>
					</Box>
				);

			case 'table':
				return <Box sx={{ p: 2 }}>{message}</Box>;

			case 'plots':
				const tableData = message?.props?.data?.data || null;
				const hasValidData = tableData && Array.isArray(tableData) && tableData.length > 0;
				console.log('hasValidData', tableData);

				return hasValidData ? (
					<Box sx={{ minHeight: '400px' }}>
						<AgChartComponent
							data={tableData}
							query_id={message?.props?.query_id || 'chart-view'}
							isTableView={false} // Force chart view
							setIsTableView={() => {}} // No-op since we're in read-only mode
							steps={message?.props?.steps || []}
							setIsTileAndNotUniqueFields={() => {}} // No-op
							isTileAndNotUniqueFields={false}
						/>
					</Box>
				) : (
					<Box sx={{ p: 2, textAlign: 'center' }}>
						<Typography color="text.secondary">
							No data available for visualization. Charts will appear automatically
							when table data is present.
						</Typography>
					</Box>
				);

			case 'analysis':
			default:
				return responseData.analysis ? (
					<Box sx={{ p: 2 }}>
						<ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
							{responseData.analysis}
						</ReactMarkdown>
					</Box>
				) : (
					<Box sx={{ p: 2, textAlign: 'center' }}>
						<Typography color="text.secondary">No analysis available</Typography>
					</Box>
				);
		}
	};

	// Extract data from message steps
	const extractResponseData = () => {
		if (!message?.props?.steps || !Array.isArray(message.props.steps)) {
			return { sqlQuery: null, analysis: null, hasData: false };
		}

		const steps = message.props.steps;
		const sqlStep = steps.find((step: any) => step.step_id === 4);
		const analysisStep = steps.find((step: any) => step.step_id === 7);

		const sqlQuery = sqlStep?.data?.generated_query?.[0]?.sql_query || null;
		const analysis = analysisStep?.data?.analysis || null;
		const tableData = message?.props?.data?.data || null;

		return {
			sqlQuery,
			analysis,
			tableData,
			hasData: !!(sqlQuery || analysis || tableData),
		};
	};

	// Custom components for ReactMarkdown
	const markdownComponents = {
		code({ node, inline, className, children, ...props }: any) {
			const match = /language-(\w+)/.exec(className || '');
			return !inline && match ? (
				<SyntaxHighlighter
					style={tomorrow}
					language={match[1]}
					PreTag="div"
					customStyle={{
						margin: '16px 0',
						borderRadius: '8px',
						fontSize: '14px',
					}}
					{...props}
				>
					{String(children).replace(/\n$/, '')}
				</SyntaxHighlighter>
			) : (
				<code
					className={className}
					style={{
						backgroundColor: '#f5f5f5',
						padding: '2px 6px',
						borderRadius: '4px',
						fontFamily: 'monospace',
						fontSize: '0.9em',
					}}
					{...props}
				>
					{children}
				</code>
			);
		},
		h1: ({ children }: any) => (
			<Typography variant="h4" component="h1" sx={{ mt: 3, mb: 2, fontWeight: 600 }}>
				{children}
			</Typography>
		),
		h2: ({ children }: any) => (
			<Typography variant="h5" component="h2" sx={{ mt: 2.5, mb: 1.5, fontWeight: 600 }}>
				{children}
			</Typography>
		),
		h3: ({ children }: any) => (
			<Typography variant="h6" component="h3" sx={{ mt: 2, mb: 1, fontWeight: 600 }}>
				{children}
			</Typography>
		),
		p: ({ children }: any) => (
			<Typography variant="body1" sx={{ mb: 2, lineHeight: 1.6 }}>
				{children}
			</Typography>
		),
		ul: ({ children }: any) => (
			<Box component="ul" sx={{ pl: 3, mb: 2 }}>
				{children}
			</Box>
		),
		ol: ({ children }: any) => (
			<Box component="ol" sx={{ pl: 3, mb: 2 }}>
				{children}
			</Box>
		),
		li: ({ children }: any) => (
			<Typography component="li" variant="body1" sx={{ mb: 0.5 }}>
				{children}
			</Typography>
		),
		blockquote: ({ children }: any) => (
			<Box
				sx={{
					borderLeft: '4px solid #e0e0e0',
					pl: 2,
					py: 1,
					my: 2,
					backgroundColor: '#f9f9f9',
					fontStyle: 'italic',
				}}
			>
				{children}
			</Box>
		),
		table: ({ children }: any) => (
			<Box sx={{ overflowX: 'auto', mb: 2 }}>
				<Box
					component="table"
					sx={{
						width: '100%',
						borderCollapse: 'collapse',
						border: '1px solid #e0e0e0',
					}}
				>
					{children}
				</Box>
			</Box>
		),
		th: ({ children }: any) => (
			<Box
				component="th"
				sx={{
					border: '1px solid #e0e0e0',
					backgroundColor: '#f5f5f5',
					p: 1,
					textAlign: 'left',
					fontWeight: 600,
				}}
			>
				{children}
			</Box>
		),
		td: ({ children }: any) => (
			<Box
				component="td"
				sx={{
					border: '1px solid #e0e0e0',
					p: 1,
				}}
			>
				{children}
			</Box>
		),
	};

	const responseData = extractResponseData();
	return (
		<>
			<Box sx={{ position: 'relative' }} display="flex" alignItems="flex-start">
				<Box>
					<img
						src="favicon-32x32.png"
						alt="Aidetic Logo"
						height="25px"
						width="25px"
						style={{
							borderRadius: '6px',
							backgroundColor: '#05445E',
							paddingBottom: '2.5px',
							paddingLeft: '2px',
						}}
					/>
				</Box>
				<Box sx={{ width: '100%' }} ml="20px">
					<Box sx={{ display: 'flex', alignItems: 'start', mb: '20px' }}>
						<Typography fontWeight="600" variant="body1">
							PrequelAI
						</Typography>

						{isProcessing && (
							<CircularProgress
								sx={{ marginTop: '6px', marginLeft: '15px' }}
								size={14}
							/>
						)}
						<Typography mx="10px" fontWeight="400" variant="h6">
							{processingMessage}
						</Typography>
					</Box>

					{responseData?.hasData ? (
						<Box
							sx={{
								border: '2px dashed #ccc',
								borderRadius: '8px',
								mb: 2,
								overflow: 'hidden',
								boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
							}}
						>
							{/* Header with Dropdown */}
							<Box
								sx={{
									backgroundColor: '#f8f9fa',
									p: 2,
									borderBottom: '1px solid #e9ecef',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'space-between',
								}}
							>
								<Typography variant="h6" fontWeight="600">
									{
										sectionOptions.find(
											(option) => option.value === selectedSection,
										)?.label
									}
								</Typography>

								<FormControl size="small" sx={{ minWidth: 200 }}>
									<Select
										value={selectedSection}
										onChange={(e) => setSelectedSection(e.target.value)}
										sx={{ backgroundColor: 'white' }}
									>
										{sectionOptions.map((option) => (
											<MenuItem key={option.value} value={option.value}>
												<Box
													sx={{
														display: 'flex',
														alignItems: 'center',
														gap: 1,
													}}
												>
													<span>{option.icon}</span>
													<span>
														{option.label.replace(/^[^\s]+ /, '')}
													</span>
												</Box>
											</MenuItem>
										))}
									</Select>
								</FormControl>
							</Box>

							{renderSectionContent()}
						</Box>
					) : (
						<Box sx={{ '& > *:first-of-type': { mt: 0 } }}>
							<ReactMarkdown
								remarkPlugins={[remarkGfm]}
								components={markdownComponents}
							>
								{typeof message === 'string' ? message : String(message)}
							</ReactMarkdown>
						</Box>
					)}
				</Box>
			</Box>

			{isProcessing && <TableLoadingSkeleton />}

			<Divider sx={{ margin: '20px 0px', ml: '44px', mb: '34px' }} light />
		</>
	);
};

export default BotChatMessage;
