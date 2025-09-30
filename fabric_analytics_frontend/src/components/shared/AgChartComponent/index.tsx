import { AgGridReact } from '@ag-grid-community/react';
import { Box, Button, CircularProgress, Stack, Typography } from '@mui/material';
import React, { /* useCallback, */ useMemo, useRef, useState } from 'react';
import {
	AgChartThemeOverrides,
	CellRangeParams,
	ChartToolPanelsDef,
	//ChartToolPanelsDef,
	ColDef,
	//RangeSelectionChangedEvent,
	SideBarDef,
} from '@ag-grid-community/core';
import _, { size } from 'lodash';
import CustomToolTip from '../CustomToolTip';
import { SvgDownLoadIcon, /* PinIcon, */ FullScreenSvgIcon } from '../AppIcons';
import { handleExportCsv } from '../../../utils/utilFunctions';
import { TEXT_CONSTANTS } from '../../../utils/TextContants';
import FullscreenExitIcon from '@mui/icons-material/FullscreenExit';
import SimpleTileChart from '../Charts/SimpleTileChart';

export const MAX_CHAT_DATA = 3000;

interface AgChartComponentProps {
	data: Record<string, string>[];
	query_id: string;
	isTableView: boolean;
	setIsTableView: any;
	steps: any;
	setIsTileAndNotUniqueFields: any;
	isTileAndNotUniqueFields: boolean;
}

const AgChartComponent = ({
	data,
	query_id,
	isTableView,
	setIsTableView,
	steps,
	setIsTileAndNotUniqueFields,
	isTileAndNotUniqueFields,
}: AgChartComponentProps) => {
	let chartRef = useRef(null);
	let gridRef = useRef<AgGridReact<any>>(null);
	const [exportData, setExportData] = React.useState<Record<string, string>[]>([]);
	const [rowData, setRowData] = useState<any[]>([]);
	const [columnDefs, setColumnDefs] = useState<ColDef[]>([]);
	const [isFullScreen, setIsFullScreen] = React.useState<boolean>(false);
	const [haveTableData, sethaveTableData] = React.useState<boolean>(true);
	const [cellRange, setCellRange] = useState<CellRangeParams | {}>({});
	const [chartParams, setChartParams] = useState<any>(null);
	const [isChartLoading, setIsChartLoading] = useState<boolean>(false);

	const gridStyle = useMemo(() => {
		if (!isFullScreen) {
			return {
				height: `${150 + size(rowData) * 52}px`,
				maxHeight: 600,
				minHeight: 400,
				width: '100%',
			};
		} else {
			return {
				height: '100vh',
				maxHeight: '100vh',
				width: '100vw',
				position: 'fixed',
				top: 0,
				left: 0,
				zIndex: 10,
			};
		}
	}, [rowData, isFullScreen]);

	const defaultColDef = useMemo<ColDef>(() => {
		return {
			flex: 1,
			enableRowGroup: true,
			enablePivot: true,
			filter: true,
			minWidth: 200,
			//minHeight: 52,
		};
	}, []);

	const popupParent = useMemo<HTMLElement | null>(() => {
		return document.body;
	}, []);

	const chartThemeOverrides = useMemo<AgChartThemeOverrides>(() => {
		return {
			bar: {
				axes: {
					category: {
						label: {
							autoRotate: true,
							autoRotateAngle: 22,
						},
					},
				},
			},
		};
	}, []);

	React.useEffect(() => {
		try {
			//TODO: below logic which converts strings
			//which are numbers to actual numbers should be updated in future
			let tempData: any = _.map(data, (row) => {
				return _.mapValues(row, function (value) {
					let isStringAndNumber: boolean = false;
					/* @ts-ignore */
					isStringAndNumber = typeof value === 'string' && !isNaN(value);
					if (isStringAndNumber) {
						return parseFloat(value);
					} else {
						return value;
					}
				});
			});

			setExportData(tempData);
			if (!Array.isArray(tempData) || tempData?.length === 0) {
				return sethaveTableData(false);
			}

			let chartType: string | null = null;
			let uniqueFields: any[] = [];
			let generateQueryObj = _.find(steps, (item) => item?.display_name === 'GenerateQuery');
			let tempIsTileAndNotUniqueFields = false;

			if (
				generateQueryObj?.data?.generated_query?.[0]?.chart?.type === null ||
				generateQueryObj?.data?.generated_query?.[0]?.chart?.type === 'null' ||
				generateQueryObj?.data?.generated_query?.[0]?.chart?.type === 'tile'
			) {
				uniqueFields = Array.from(tempData?.flatMap(Object.keys));

				if (
					_.size(uniqueFields) > 1 &&
					_.findIndex(uniqueFields, (itm, index) => {
						if (index === 0) {
							return false;
						}
						return itm === uniqueFields[0];
					}) !== -1
				) {
					setIsTileAndNotUniqueFields(true);
					setIsTableView(true);
					uniqueFields = Array.from(new Set(tempData?.flatMap(Object.keys)));
				}
			} else {
				uniqueFields = Array.from(new Set(tempData?.flatMap(Object.keys)));
			}

			let tempUniqueFields = [...uniqueFields];

			if (generateQueryObj) {
				chartType = generateQueryObj?.data?.generated_query?.[0]?.chart?.type ?? null;
				let genQuery = generateQueryObj?.data?.generated_query?.[0]?.chart;

				if (
					chartType !== null &&
					chartType !== 'null' &&
					chartType !== 'tile' &&
					_.size(genQuery?.x_axis) > 0 &&
					_.size(genQuery?.y_axis) > 0
				) {
					tempUniqueFields = [...genQuery?.x_axis, ...genQuery?.y_axis];
				}
			}

			setCellRange({
				columns: tempUniqueFields,
			});

			const columns: any[] = uniqueFields?.map((field) => {
				if (
					!tempIsTileAndNotUniqueFields &&
					_.size(generateQueryObj?.data?.generated_query?.[0]?.chart?.x_axis) > 0 &&
					_.size(generateQueryObj?.data?.generated_query?.[0]?.chart?.y_axis) > 0
				) {
					let foundIndex = -1;
					foundIndex = _.findIndex(
						generateQueryObj?.data?.generated_query?.[0]?.chart?.x_axis,
						(itm) => itm === field,
					);

					let foundIndex2 = -1;
					foundIndex2 = _.findIndex(
						generateQueryObj?.data?.generated_query?.[0]?.chart?.y_axis,
						(itm) => itm === field,
					);
					if (foundIndex !== -1) {
						return {
							field,
							chartDataType: 'category',
						};
					} else if (foundIndex2 !== -1) {
						return {
							field,
							chartDataType: 'series',
						};
					}
					return {
						field,
						chartDataType: 'excluded',
					};
				} else {
					return {
						field,
					};
				}
			});

			if (_.size(tempData) > MAX_CHAT_DATA) {
				setIsTableView(true);
			}

			setColumnDefs(columns);

			setRowData(tempData);
		} catch (e) {
			console.log(e);
		}
	}, [data, setIsTableView]);

	React.useEffect(() => {
		if (
			chartRef.current === null &&
			chartParams !== null &&
			isTileAndNotUniqueFields === false
		) {
			setIsChartLoading(true);
			chartRef.current = chartParams.api.createRangeChart({
				chartContainer: document.querySelector(`#myChart-${query_id}`) as any,
				cellRange: cellRange,
				suppressChartRanges: true,
				chartType: 'groupedColumn',
				aggFunc: 'sum',
			});
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [isTableView, setIsChartLoading]);

	const sideBar = useMemo<SideBarDef | string | string[] | boolean | null>(() => {
		return {
			toolPanels: [
				{
					id: 'columns',
					labelDefault: 'Columns',
					labelKey: 'columns',
					iconKey: 'columns',
					toolPanel: 'agColumnsToolPanel',
				},
			],
			defaultToolPanel: undefined,
		};
	}, []);

	const { botResponseText, chartType }: any = useMemo(() => {
		let generateQueryObj = _.find(steps, (item) => item?.display_name === 'GenerateQuery');
		let returnText = '';
		let chartType: string | null = null;
		if (generateQueryObj) {
			returnText = generateQueryObj?.data?.generated_query?.[0]?.response;
			chartType = generateQueryObj?.data?.generated_query?.[0]?.chart?.type ?? null;
		}
		return { botResponseText: returnText, chartType };
	}, [steps]);

	function onFirstDataRendered(params: any) {
		if (isTableView === false) {
			chartRef.current = params.api.createRangeChart({
				chartContainer: document.querySelector(`#myChart-${query_id}`) as any,
				cellRange: cellRange,
				suppressChartRanges: true,
				chartType:
					chartType === null || chartType === 'null' || chartType === 'tile'
						? 'groupedColumn'
						: chartType,
				aggFunc: 'sum',
				chartThemeOverrides: {
					common: {
						background: {
							fill: 'transparent',
						},
						axes: {
							category: {
								gridLine: {
									style: {
										lineDash: [3, 3],
										stroke: '#ccc',
									},
								},
							},
						},
					},
				},
				//commenting below line as it was throwing runtime error FAB-55
				/* chartThemeOverrides: {
				common: {
					defaultToolPanel: 'settings',
				},
				}
			}, */
			});
		} else {
			setChartParams(params);
		}
	}

	const chartToolPanelsDef = useMemo<ChartToolPanelsDef>(() => {
		return {
			settingsPanel: {
				chartGroupsDef: {
					pieGroup: ['doughnut', 'pie'],
					columnGroup: ['column'],
					barGroup: ['bar'],
					lineGroup: ['line'],
				},
			},
		};
	}, [isTableView]);

	/* const onRangeSelectionChanged = useCallback((event: RangeSelectionChangedEvent) => {
		var cellRanges = gridRef.current!.api.getCellRanges();
		if (chartRef.current) {
		}
	}, []); */

	return (
		<Box
			sx={{
				width: '100%',
				height: '100%',
				display: 'flex',
				flexDirection: 'column',
			}}
		>
			{botResponseText !== '' ? (
				<Typography variant="secTitle" lineHeight="20px">
					{botResponseText}
				</Typography>
			) : null}
			<Box
				sx={{
					display: 'flex',
					alignItems: 'center',
					marginLeft: 'auto',
					marginBottom: '10px',
				}}
			>
				{chartType !== 'null' &&
					chartType !== 'tile' &&
					chartType !== null &&
					haveTableData && (
						<CustomToolTip
							title={
								!isFullScreen
									? TEXT_CONSTANTS.CHAT_SESSION_PAGE_FULL_SCREEN
									: TEXT_CONSTANTS.CHAT_SESSION_PAGE_MINIMIZE
							}
						>
							<Button
								onClick={() => setIsFullScreen((prev) => !prev)}
								sx={
									!isFullScreen
										? {
												background: 'transparent',
												color: '#5E5468',
												padding: '6px',
												minWidth: 'auto',
												border: '0.5px solid transparent',
												'&:hover': {
													background: 'rgba(255, 255, 255, 0.15)',
													border: '0.5px solid #CBBCDC',
												},
												'&:before': {
													display: 'none',
												},
											}
										: isTableView
											? {
													marginRight: '5px',
													position: 'fixed',
													right: '20px',
													top: '6px',
													zIndex: 11,
													background: 'transparent',
													color: '#5E5468',
													padding: '6px',
													minWidth: 'auto',
													border: '0.5px solid transparent',
													'&:hover': {
														background: 'rgba(255, 255, 255, 0.15)',
														border: '0.5px solid #CBBCDC',
													},
													'&:before': {
														display: 'none',
													},
												}
											: {
													position: 'fixed',
													left: '20px',
													top: '6px',
													zIndex: 11,
													background: 'transparent',
													color: '#5E5468',
													padding: '6px',
													minWidth: 'auto',
													border: '0.5px solid transparent',
													'&:hover': {
														background: 'rgba(255, 255, 255, 0.15)',
														border: '0.5px solid #CBBCDC',
													},
													'&:before': {
														display: 'none',
													},
												}
								}
								className="icon-with20px-h-w"
							>
								{!isFullScreen ? (
									<FullScreenSvgIcon />
								) : (
									<FullscreenExitIcon
										sx={{ fontSize: '20px', color: '#5E5468' }}
									/>
								)}
							</Button>
						</CustomToolTip>
					)}
				{haveTableData && (
					<CustomToolTip title={TEXT_CONSTANTS.CHAT_SESSION_PAGE_DOWNLOAD}>
						<Button
							onClick={() => {
								handleExportCsv(exportData);
							}}
							sx={{
								background: 'transparent',
								color: '#5E5468',
								padding: '6px',
								minWidth: 'auto',
								border: '0.5px solid transparent',
								'&:hover': {
									background: 'rgba(255, 255, 255, 0.15)',
									border: '0.5px solid #CBBCDC',
								},
								'&:before': {
									display: 'none',
								},
							}}
							className="icon-with20px-h-w"
						>
							<SvgDownLoadIcon />
						</Button>
					</CustomToolTip>
				)}
				{/* {haveTableData && (
					<CustomToolTip>
						<Button
							onClick={() => {
								//setShowSteps(!showSteps);
							}}
							sx={{
								background: 'transparent',
								color: '#5E5468',
								padding: '6px',
								minWidth: 'auto',
								marginRight: '10px',
								border: '0.5px solid transparent',
								'&:hover': {
									background: 'rgba(255, 255, 255, 0.15)',
									border: '0.5px solid #CBBCDC',
								},
								'&:before': {
									display: 'none',
								},
							}}
							className="icon-with20px-h-w chat-page-pin-icon"
						>
							<PinIcon />
						</Button>
					</CustomToolTip>
				)} */}
			</Box>
			<Box
				sx={{
					width: '100%',
					height: '100%',
					display: 'flex',
					flexDirection: 'column',
				}}
			>
				<div
					id="myGrid"
					/* @ts-ignore */
					style={
						!isTileAndNotUniqueFields &&
						(chartType === 'null' || chartType === 'tile' || chartType === null)
							? {}
							: isTableView
								? gridStyle
								: { position: 'absolute' }
					}
					className={'ag-theme-quartz'}
				>
					{isTileAndNotUniqueFields === false &&
					(chartType === 'null' || chartType === 'tile' || chartType === null) ? (
						<Stack gap="12px">
							{_.size(rowData) > 0 ? (
								_.map(
									_.size(rowData) > 0 ? rowData?.[0] : [],
									(item, k: string) => {
										if (typeof item === 'string' || typeof item === 'number') {
											return (
												<SimpleTileChart key={k} title={k} value={item} />
											);
										}

										return (
											<SimpleTileChart
												key={k}
												title={k}
												value={'Data not found!'}
											/>
										);
									},
								)
							) : (
								<SimpleTileChart title={'No data'} value={'Data not found!'} />
							)}
						</Stack>
					) : (
						<AgGridReact
							ref={gridRef}
							rowData={rowData}
							columnDefs={columnDefs}
							defaultColDef={defaultColDef}
							enableRangeSelection={true}
							popupParent={popupParent}
							enableCharts={true}
							chartThemeOverrides={chartThemeOverrides}
							suppressMultiRangeSelection={true}
							rowHeight={50}
							headerHeight={48}
							suppressRowClickSelection={true}
							groupSelectsChildren={true}
							rowSelection={'multiple'}
							rowGroupPanelShow={'always'}
							pivotPanelShow={'always'}
							pagination={true}
							paginationPageSize={10}
							paginationPageSizeSelector={[10, 20, 50, 100]}
							sideBar={sideBar}
							className={
								(isFullScreen ? ' ag-full-screen' : '') +
								(isTableView ? ' ag-table-view' : ' ag-chart-view')
							}
							onFirstDataRendered={onFirstDataRendered}
							//commenting below line as it was throwing runtime error FAB-55
							chartToolPanelsDef={isTableView === true ? {} : chartToolPanelsDef}
							//onRangeSelectionChanged={onRangeSelectionChanged}
							//commenting below line as it was throwing runtime error FAB-55
							//onChartCreated={onChartCreated}
							enableRangeHandle={true}
						/>
					)}
				</div>
				{!isTileAndNotUniqueFields &&
				(chartType === 'null' || chartType === 'tile' || chartType === null) ? null : (
					<div
						id={`myChart-${query_id}`}
						className={
							'ag-theme-quartz my-chart' + (isFullScreen ? ' ag-full-screen' : '')
						}
						style={
							isTableView
								? { maxWidth: 0, maxHeight: 0 }
								: isFullScreen
									? {
											height: '100vh',
											minHeight: '100vh',
											width: '100%',
											position: 'fixed',
											top: 0,
											left: 0,
											zIndex: 10,
										}
									: {
											height: `${150 + size(rowData) * 52}px`,
											minHeight: 600,
											maxHeight: 600,
											width: '100%',
											position: 'relative',
										}
						}
					>
						{isChartLoading && (
							<Stack
								flexDirection="column"
								justifyContent="center"
								alignItems="center"
								width="100%"
								height="100%"
								sx={{
									background: 'white',
									position: 'absolute',
									borderRadius: '8px',
									top: 0,
									left: 0,
									right: 0,
									bottom: 0,
									zIndex: 1,
								}}
							>
								<CircularProgress color="secondary" disableShrink />
							</Stack>
						)}
					</div>
				)}
			</Box>
		</Box>
	);
};

export default AgChartComponent;
