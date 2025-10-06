import _ from 'lodash';

/**
 *
 * function to download passed data as csv on browser
 */
export const handleExportCsv = (data: any) => {
	let csvData = data?.map(
		(entry: any) =>
			Object.values(entry)
				?.map((value) => (value ? value.toString() : ''))
				.join(','),
	);

	let header =
		Object.keys(data?.[0] ?? {})
			?.map((value: string) => value.toString())
			?.join(',') ?? '';

	csvData = [header, ...csvData];

	const blob = new Blob([csvData?.join('\n')], { type: 'text/csv;charset=utf-8;' });
	const link = document.createElement('a');
	const url = URL.createObjectURL(blob);
	link.href = url;
	link.download = 'table.csv';
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
};

/**
 *
 * function to format Indian number to long compact value with currency style.
 * maxfraction digits converted to two decimal places.
 */
export const formatToIndianNumber = new Intl.NumberFormat('en-IN', {
	style: 'currency',
	currency: 'INR',
	minimumFractionDigits: 0,
	maximumFractionDigits: 2,
	notation: 'compact',
	compactDisplay: 'long',
});

/**
 *
 * function to format Indian number to long format value with currency style.
 */
export const formatToIndianNumberLong = new Intl.NumberFormat('en-IN', {
	style: 'currency',
	currency: 'INR',
	minimumFractionDigits: 0,
	maximumFractionDigits: 2,
});

/**
 *
 * function to convert T to K for thousands for compact formatted indian number.
 */
export const convertTToKNummber = (value: string) => {
	return value.replace('T', 'K');
};

/**
 *
 * function to get keys along with data type and sample value
 */
export const getObjectKeysWithDataType = (object: any | object) => {
	return Object.keys(object).map((key) => {
		return { key: key, data_type: typeof object[key], sample_value: object[key] };
	});
};

/**
 * Hex colors dinstinct to huemn eye for chart colors
 */
export const distinctHexColors = [
	'#5A7AF9',
	'#F77C7C',
	'#E5C05E',
	'#6DDE6A',
	'#E19359',
	'#6EC6CD',
	'#C791F1',
	'#C1C1C1',
];
/* [
	'#5A7AF9',
	'#F95A9D',
	'#7AF95D',
	'#F9B15A',
	'#F95D5A',
	'#5AF9C7',
	'#E75AF9',
	'#F9E45A',
	'#9DF95A',
	'#F95AA3',
	'#5A9DF9',
	'#9A5AF9',
	'#F95A5A',
	'#5AF995',
	'#F97A5A',
	'#5AF9E4',
	'#F95D95',
	'#5A5AF9',
	'#E4F95A',
	'#F95A9A',
	'#5A7AF9',
	'#F95A9D',
	'#7AF95D',
	'#F9B15A',
	'#F95D5A',
	'#5AF9C7',
	'#E75AF9',
	'#F9E45A',
	'#9DF95A',
	'#F95AA3',
	'#5A9DF9',
	'#9A5AF9',
	'#F95A5A',
	'#5AF995',
	'#F97A5A',
	'#5AF9E4',
	'#F95D95',
	'#5A5AF9',
	'#E4F95A',
	'#F95A9A',
	'#5A7AF9',
	'#F95A9D',
	'#7AF95D',
	'#F9B15A',
	'#F95D5A',
	'#5AF9C7',
	'#E75AF9',
	'#F9E45A',
	'#9DF95A',
	'#F95AA3',
	'#5A9DF9',
	'#9A5AF9',
	'#F95A5A',
	'#5AF995',
	'#F97A5A',
	'#5AF9E4',
	'#F95D95',
	'#5A5AF9',
	'#E4F95A',
	'#F95A9A',
	'#5A7AF9',
	'#F95A9D',
	'#7AF95D',
	'#F9B15A',
	'#F95D5A',
	'#5AF9C7',
	'#E75AF9',
	'#F9E45A',
	'#9DF95A',
	'#F95AA3',
	'#5A9DF9',
	'#9A5AF9',
	'#F95A5A',
	'#5AF995',
	'#F97A5A',
	'#5AF9E4',
	'#F95D95',
	'#5A5AF9',
	'#E4F95A',
	'#F95A9A',
	'#5A7AF9',
	'#F95A9D',
	'#7AF95D',
	'#F9B15A',
	'#F95D5A',
	'#5AF9C7',
	'#E75AF9',
	'#F9E45A',
	'#9DF95A',
	'#F95AA3',
	'#5A9DF9',
	'#9A5AF9',
	'#F95A5A',
	'#5AF995',
	'#F97A5A',
	'#5AF9E4',
	'#F95D95',
	'#5A5AF9',
	'#E4F95A',
	'#F95A9A',
]; */

/* constant used for formatTileNumber function */
export const TILE_VALUE_FORMAT_METRICS = ['cost', 'revenue', 'sale', 'turnover', 'spend', 'value'];

/**
 * This  function converts passed value into formatted value either rupee prefixed or not
 * based on metric passed. If decimal places are there, it will be rounded to 2 decimal places only.
 *
 * @param value - value to format
 * @param metric - metric based on this string value value will show rupee symbol or not
 * @returns - formatted value
 */
export const formatTileNumber = (value: any, metric: string) => {
	let returnValue = value;

	let isRate = metric.toLowerCase().includes('rate');

	if (isRate) {
		returnValue = `${
			`${returnValue * 100}`.includes('.')
				? (returnValue * 100).toFixed(2)
				: returnValue * 100
		}%`;

		return returnValue;
	}

	returnValue = `${formatToIndianNumberLong.format(
		`${value}`.includes('.') ? value.toFixed(2) : value,
	)}`;

	let isCurrency = false;
	let isPercent = metric.toLowerCase().includes('percent');

	if (!isPercent) {
		isCurrency = _.some(TILE_VALUE_FORMAT_METRICS, (item) => {
			return metric.toLowerCase().includes(item.toLowerCase());
		});
	}

	if (isPercent) {
		returnValue = `${returnValue}%`;
	}

	return returnValue.replaceAll('₹', '');
};

/**
 * Converts a URLSearchParams object into a JavaScript object containing all key-value pairs.
 * @param {URLSearchParams} searchParams - The URLSearchParams object to convert.
 * @returns {Object} - An object containing all key-value pairs from the URLSearchParams object.
 */
export const urlSearchParamsToObject = (searchParams: any) => {
	const obj: any = {};

	searchParams.forEach((value: any, key: any) => {
		obj[key] = value;
	});

	return obj;
};

export const isJsonString = (str: string) => {
	try {
		JSON.parse(str);
	} catch (e) {
		return false;
	}
	return true;
};

/* Access list for customers */
export const ACCESS_LIST = ['fabric_access_id_5123', 'prequel_ai_4521', 'presales_demo_ecom','presales_demo_loan','databricks_sql_test'];
