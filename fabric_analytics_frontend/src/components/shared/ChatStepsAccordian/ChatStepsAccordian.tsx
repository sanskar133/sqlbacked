import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Box } from '@mui/system';
import { StepData } from '../../../types/apis/socket';
import { format as prettyFormat } from 'pretty-format';
import _ from 'lodash';

const SEPARATOR = ',';
const serializeItems: any = (
	items: any,
	config: any,
	indentation: any,
	depth: any,
	refs: any,
	printer: any,
) => {
	if (items.length === 0) {
		return '';
	}
	const indentationItems = indentation + config.indent;
	return (
		config.spacingOuter +
		items
			.map(
				(item: any) =>
					indentationItems + printer(item, config, indentationItems, depth, refs), // callback
			)
			.join(SEPARATOR + config.spacingInner) +
		(config.min ? '' : SEPARATOR) + // following the last item
		config.spacingOuter +
		indentation
	);
};

const serializeObjectItems: any = (
	items: any,
	config: any,
	indentation: any,
	depth: any,
	refs: any,
	printer: any,
) => {
	if (_.size(items) === 0) {
		return '';
	}
	const indentationItems = indentation + config.indent;
	return (
		config.spacingOuter +
		_.map(
			items,
			(item: any, key: string) =>
				indentationItems +
				`"${key}": ` +
				printer(item, config, indentationItems, depth, refs), // callback
		).join(SEPARATOR + config.spacingInner) +
		(config.min ? '' : SEPARATOR) + // following the last item
		config.spacingOuter +
		indentation
	);
};

/* const serializeStringItems: any = (
	items: any,
	config: any,
	indentation: any,
	depth: any,
	refs: any,
	printer: any,
) => {
	if (_.size(items) === 0) {
		return '';
	}
	const indentationItems = indentation + config.indent;
	return _.map(items.split('\n'), (item: any) => item).join(config.spacingInner);
}; */

const plugin: any = {
	test(val: any) {
		return Array.isArray(val);
	},
	serialize(array: any, config: any, indentation: any, depth: any, refs: any, printer: any) {
		const name = array.constructor.name;
		return ++depth > config.maxDepth
			? `[${name}]`
			: `[${serializeItems(array, config, indentation, depth, refs, printer)}]`;
	},
};

const plugin2: any = {
	test(val: any) {
		return typeof val === 'object';
	},
	serialize(object: any, config: any, indentation: any, depth: any, refs: any, printer: any) {
		const name = object?.constructor?.name;
		return ++depth > config.maxDepth
			? `{${name}}`
			: `{${serializeObjectItems(object, config, indentation, depth, refs, printer)}}`;
	},
};

/* const plugin3: any = {
	test(val: any) {
		return typeof val === 'string';
	},
	serialize(str: any, config: any, indentation: any, depth: any, refs: any, printer: any) {
		const name = str?.constructor?.name;
		return ++depth > config.maxDepth
			? `{${name}}`
			: _.size(str.trim().split('\n')) === 0 && _.size(str.trim().split('\t')) === 0
				? str
				: `${serializeStringItems(str, config, indentation, depth, refs, printer)}`;
	},
}; */

const ChatStepsAccordian = ({ steps }: { steps: StepData[] }) => {
	return (
		<Box my="20px">
			{steps?.map((el: StepData, index) => {
				//const formattedJson = JSON.stringify(el.data, null, 2);
				return (
					<Accordion
						key={index}
						disableGutters={true}
						TransitionProps={{ timeout: { appear: 1, enter: 1, exit: 4 } }}
					>
						<AccordionSummary
							expandIcon={<ExpandMoreIcon />}
							aria-controls="panel1a-content"
							id="panel1a-header"
						>
							<Typography>{el.display_name}</Typography>
						</AccordionSummary>
						<AccordionDetails>
							<Typography>{el.message}</Typography>

							<Typography variant="subtitle2">
								<pre style={{ whiteSpace: 'pre-wrap' }}>
									{prettyFormat(el.data, {
										escapeString: false,
										plugins: [plugin, plugin2],
									})}
									{/* {formattedJson} */}
								</pre>
							</Typography>
						</AccordionDetails>
					</Accordion>
				);
			})}
		</Box>
	);
};

export default ChatStepsAccordian;
