import * as React from 'react';
import Typography, { TypographyProps } from '@mui/material/Typography';
import { Box, Grid, TextField, TextFieldPropsSizeOverrides, Tooltip } from '@mui/material';
import { RoundedInfoSvgIcon } from '../AppIcons';

interface Props {
	label?: string;
	value: string;
	setValue(value: string): void;
	fullWidth?: boolean;
	tooltip?: string;
	placeholder?: string;
	labelProps?: TypographyProps;
	size?: string;
	error?: boolean;
	helperText?: string;
}

/**
 * Return a customized Input element, with label and info tooltip (not mandatory)
 * @param
 * @returns JSX element
 */
const CustomInput: React.FC<Props> = ({
	setValue,
	value,
	fullWidth,
	label,
	tooltip,
	placeholder,
	labelProps,
	size = 'small',
	error = false,
	helperText = '',
}) => {
	return (
		<Grid item container flexDirection={'column'} gap={'6px'}>
			{label && (
				<Grid item>
					<Typography {...labelProps}>{label}</Typography>
					{tooltip && (
						<Tooltip title={tooltip}>
							<Box>
								<RoundedInfoSvgIcon />
							</Box>
						</Tooltip>
					)}
				</Grid>
			)}
			<Grid item>
				<TextField
					fullWidth={fullWidth}
					//@ts-ignore
					size={size}
					type="text"
					InputLabelProps={{ shrink: true }}
					value={value}
					onChange={(e) => {
						setValue(e.target.value);
					}}
					placeholder={placeholder}
					sx={{
						'& .MuiOutlinedInput-root': {
							background:
								'linear-gradient(180deg, rgba(255, 255, 255, 0.60) 0%, rgba(255, 255, 255, 0.60) 33.65%, rgba(255, 255, 255, 0.60) 65.42%, rgba(255, 255, 255, 0.60) 100%)',
						},
					}}
					helperText={helperText}
					error={error}
				/>
			</Grid>
		</Grid>
	);
};

export default CustomInput;
