import React, { useEffect, useState } from 'react';
import { Box, Button, Tab, Tabs, Typography } from '@mui/material';
import ChatStepsAccordian from '../ChatStepsAccordian/ChatStepsAccordian';
import { BoardBookIcon, TableIcon, ChartIcon } from '../AppIcons';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import '@ag-grid-community/styles/ag-grid.css';
import '@ag-grid-community/styles/ag-theme-quartz.css';
import { ModuleRegistry } from '@ag-grid-community/core';
import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { MenuModule } from '@ag-grid-enterprise/menu';
import { GridChartsModule } from '@ag-grid-enterprise/charts';
import { RowGroupingModule } from '@ag-grid-enterprise/row-grouping';
import { ClipboardModule } from '@ag-grid-enterprise/clipboard';
import { StatusBarModule } from '@ag-grid-enterprise/status-bar';
import { SideBarModule } from '@ag-grid-enterprise/side-bar';
//import { AdvancedFilterModule } from '@ag-grid-enterprise/advanced-filter';
import { ColumnsToolPanelModule } from '@ag-grid-enterprise/column-tool-panel';
import { RichSelectModule } from '@ag-grid-enterprise/rich-select';
//import { ExcelExportModule } from '@ag-grid-enterprise/excel-export';
import CustomToolTip from '../../shared/CustomToolTip';
import { TEXT_CONSTANTS } from '../../../utils/TextContants';
import AgChartComponent from '../AgChartComponent';
import _ from 'lodash';

const { CHAT_SESSION_PAGE_TABLE_VIEW, CHAT_SESSION_PAGE_CHART_VIEW, CHAT_SESSION_PAGE_STEPS } =
	TEXT_CONSTANTS;

// Register the required feature modules with the Grid
ModuleRegistry.registerModules([
	ClientSideRowModelModule,
	MenuModule,
	GridChartsModule,
	RowGroupingModule,
	ClipboardModule,
	StatusBarModule,
	SideBarModule,
	//AdvancedFilterModule,
	RichSelectModule,
	//ExcelExportModule,
	ColumnsToolPanelModule,
]);

interface DynamicTableProps {
	data: Record<string, string>[] | any;
	steps: any[];
	query_id: string;
	isAdmin: boolean;
	followup?: string | undefined;
}

function TabPanel(props: any) {
	const { children, value, index, ...other } = props;

	return (
		<div
			role="tabpanel"
			hidden={value !== index}
			id={`simple-tabpanel-${index}`}
			aria-labelledby={`simple-tab-${index}`}
			{...other}
		>
			{value === index && <Box sx={{ p: 3 }}>{children}</Box>}
		</div>
	);
}

function a11yProps(index: any) {
	return {
		id: `simple-tab-${index}`,
		'aria-controls': `simple-tabpanel-${index}`,
	};
}

const DynamicTableWithStepsComponent: React.FC<DynamicTableProps> = ({
	data,
	steps,
	query_id,
	isAdmin,
	followup = undefined,
}) => {
	const [showSteps, setShowSteps] = React.useState<boolean>(false);
	const [haveTableData, sethaveTableData] = React.useState<boolean>(true);
	const [isTableView, setIsTableView] = React.useState<boolean>(false);
	const [activeTab, setActiveTab] = useState(0);
	const [isTileAndNotUniqueFields, setIsTileAndNotUniqueFields] = useState<boolean>(false);

	const handleChange = (event: any, newValue: any) => {
		setActiveTab(newValue);
	};

	const getStepData = (steps: any[], displayName: any) => {
		const step: any = steps.find((step) => step.display_name === displayName);
		return step ? step.data : null;
	};
	const assistant_step_data = getStepData(steps, 'TriggerAssistantForAnalytics');

	useEffect(() => {
		if (!data) {
			sethaveTableData(false);
		}
		if (Array.isArray(data?.data) && data?.data?.length === 0) {
			sethaveTableData(false);
		}
	}, [data]);

	return (
		<Box sx={{ width: '100%', position: 'relative' /* marginTop: '100px' */ }}>
			<Box
				sx={{
					top: '-50px',
					right: '0px',
					position: 'absolute',
					display: 'flex',
					alignItems: 'center',
				}}
			>
				{isAdmin && (
					<CustomToolTip title={CHAT_SESSION_PAGE_STEPS}>
						<Button
							onClick={() => {
								setShowSteps(!showSteps);
							}}
							sx={{
								fontSize: '14px',
								fontWeight: 400,
								background: showSteps ? 'rgba(255, 255, 255, 0.15)' : 'transparent',
								color: '#5E5468',
								padding: '6px',
								minWidth: 'auto',
								marginBlock: '0px',
								marginRight: '4px',
								border: showSteps
									? '0.5px solid #CBBCDC'
									: '0.5px solid transparent',
								textTransform: 'capitalize',
								'&:hover': {
									background: 'rgba(255, 255, 255, 0.15)',
									border: '0.5px solid #CBBCDC',
									color: '#5E5468',
								},
								'&:before': {
									display: 'none',
								},
							}}
						>
							<BoardBookIcon />
						</Button>
					</CustomToolTip>
				)}

				{!isTileAndNotUniqueFields && haveTableData && followup === undefined && (
					<ToggleButtonGroup
						value={isTableView}
						exclusive
						onChange={() => setIsTableView(!isTableView)}
						aria-label="choose view type chart view or table"
						size="small"
						sx={{
							marginRight: '5px',
							borderRadius: '8px',
							height: '32px',
							width: '64px',
						}}
					>
						<CustomToolTip title={CHAT_SESSION_PAGE_CHART_VIEW}>
							<ToggleButton
								value={false}
								aria-label="chart view"
								sx={{
									borderRadius: '8px 0px 0px 8px',
									borderTop: '0.5px solid #CBBCDC',
									borderBottom: '0.5px solid #CBBCDC',
									borderLeft: '0.5px solid #CBBCDC',
									background: !isTableView
										? 'rgba(255, 255, 255, 0.50)'
										: 'rgba(255, 255, 255, 0.15)',
									'&:hover': {
										background: !isTableView
											? 'rgba(255, 255, 255, 0.50)'
											: 'rgba(255, 255, 255, 0.15)',
									},
								}}
							>
								<ChartIcon />
							</ToggleButton>
						</CustomToolTip>
						<CustomToolTip title={CHAT_SESSION_PAGE_TABLE_VIEW}>
							<ToggleButton
								value={true}
								aria-label="table view"
								sx={{
									borderRadius: '0px 8px 8px 0px',
									borderTop: '0.5px solid #CBBCDC',
									borderBottom: '0.5px solid #CBBCDC',
									borderLeft: '0.5px solid #CBBCDC',
									background: isTableView
										? 'rgba(255, 255, 255, 0.50)'
										: 'rgba(255, 255, 255, 0.15)',
									'&:hover': {
										background: isTableView
											? 'rgba(255, 255, 255, 0.50)'
											: 'rgba(255, 255, 255, 0.15)',
									},
								}}
							>
								<TableIcon />
							</ToggleButton>
						</CustomToolTip>
					</ToggleButtonGroup>
				)}
			</Box>

			{steps?.length !== 0 && showSteps && isAdmin && <ChatStepsAccordian steps={steps} />}

			{followup === undefined && (
				<>
					{haveTableData ? (
						<>
							{Array.isArray(data) ? (
								<Box>
									<Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
										<Tabs
											value={activeTab}
											onChange={handleChange}
											aria-label="data tabs"
										>
											{data?.map((el, index) => (
												<Tab
													label={`Output ${index + 1}`}
													{...a11yProps(index)}
													key={index}
												/>
											))}
										</Tabs>
									</Box>
									{data?.map((el: any, index) => (
										<TabPanel value={activeTab} index={index} key={index}>
											<AgChartComponent
												isTableView={isTableView}
												data={el?.data}
												query_id={query_id}
												setIsTableView={setIsTableView}
												steps={steps}
												setIsTileAndNotUniqueFields={
													setIsTileAndNotUniqueFields
												}
												isTileAndNotUniqueFields={isTileAndNotUniqueFields}
											/>
										</TabPanel>
									))}
								</Box>
							) : (
								<>
									<AgChartComponent
										isTableView={isTableView}
										data={data?.data}
										query_id={query_id}
										setIsTableView={setIsTableView}
										steps={steps}
										setIsTileAndNotUniqueFields={setIsTileAndNotUniqueFields}
										isTileAndNotUniqueFields={isTileAndNotUniqueFields}
									/>
								</>
							)}
						</>
					) : (
						<Box sx={{ marginTop: showSteps ? '50px' : '20px' }}>
							<Typography variant="h6">No valid data found</Typography>
						</Box>
					)}
				</>
			)}
			{followup !== undefined ? (
				<Typography variant="secTitle" lineHeight="20px">
					{followup}
				</Typography>
			) : null}
			<br></br>
			{followup === undefined && (
				<Typography variant="subtitle1">{assistant_step_data?.answer}</Typography>
			)}
		</Box>
	);
};

export default DynamicTableWithStepsComponent;
