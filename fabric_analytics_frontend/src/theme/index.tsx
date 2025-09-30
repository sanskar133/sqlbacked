import { createTheme } from '@mui/material/styles';
import type {} from '@mui/x-data-grid/themeAugmentation';
import { ChevronDownIcon, DownChevronSmall } from '../components/shared/AppIcons';

declare module '@mui/material/styles' {
	interface TypographyVariants {
		customPrmH6?: React.CSSProperties;
		prmTitle?: React.CSSProperties;
		secTitle?: React.CSSProperties;
		secMediumSmallLight?: React.CSSProperties;
		customPrmH6Bold?: React.CSSProperties;
		prmNormal?: React.CSSProperties;
		secSmall?: React.CSSProperties;
		customPrmH5?: React.CSSProperties;
		secSmallLight?: React.CSSProperties;
		customPrmH4?: React.CSSProperties;
		customBodySec?: React.CSSProperties;
	}

	// allow configuration using `createTheme`
	interface TypographyVariantsOptions {
		customPrmH6?: React.CSSProperties;
		prmTitle?: React.CSSProperties;
		secTitle?: React.CSSProperties;
		secMediumSmallLight?: React.CSSProperties;
		customPrmH6Bold?: React.CSSProperties;
		prmNormal?: React.CSSProperties;
		secSmall?: React.CSSProperties;
		customPrmH5?: React.CSSProperties;
		secSmallLight?: React.CSSProperties;
		customPrmH4?: React.CSSProperties;
		customBodySec?: React.CSSProperties;
	}
}

// Update the Typography's variant prop options
declare module '@mui/material/Typography' {
	interface TypographyPropsVariantOverrides {
		customPrmH6: true;
		prmTitle: true;
		secTitle: true;
		secMediumSmallLight: true;
		customPrmH6Bold: true;
		prmNormal: true;
		secSmall: true;
		customPrmH5: true;
		secSmallLight: true;
		customPrmH4: true;
		customBodySec: true;
	}
}

export const theme = createTheme({
	palette: {
		primary: {
			main: '#A264E0', // A shade of orange
		},
		grey: {
			A100: '#E4E7EC',
		},
		success: {
			main: '#027A48',
		},
	},
	typography: {
		fontFamily: ["'DM Sans', 'Source Sans 3', sans-serif"].join(','),
		h1: {},
		h2: {},
		h3: {
			color: '#101828',
			fontSize: '30px',
			fontStyle: 'normal',
			fontWeight: '500',
			lineHeight: '38px',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		h4: {
			color: '#101828',
			fontSize: '24px',
			fontStyle: 'normal',
			fontWeight: '500',
			lineHeight: '24px',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		h5: {
			color: '#133447',
			fontSize: '18px',
			fontStyle: 'normal',
			fontWeight: '500',
			lineHeight: '26px',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		h6: {
			color: '#5E5468',
			fontSize: '16px',
			fontStyle: 'normal',
			fontWeight: '500',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		subtitle1: {
			color: '#5E5468',
			fontSize: '14px',
			fontStyle: 'normal',
			fontWeight: '500',
			lineHeight: '16px',

			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		subtitle2: {
			color: '#5E5468',
			fontSize: '13px',
			fontStyle: 'normal',
			fontWeight: '500',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
			lineHeight: '20px',
		},
		caption: {
			color: '#667085',
			fontSize: '14px',
			fontStyle: 'normal',
			fontWeight: '400',
			lineHeight: '20px',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		body1: {
			color: '#0E1118',
			fontSize: '18px',
			fontStyle: 'normal',
			fontWeight: '500',
			lineHeight: '26px',

			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		body2: {
			color: '#101828',
			fontSize: '22px',
			fontStyle: 'normal',
			fontWeight: '600',
			fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
		},
		customPrmH6: {
			fontFamily: 'DM Sans',
			fontSize: '18px',
			fontWeight: 500,
			lineHeight: '26px',
			color: '#101828',
		},
		prmTitle: {
			fontFamily: 'DM Sans',
			fontSize: '16px',
			fontWeight: 500,
			lineHeight: '26px',
			color: '#101828',
		},
		secTitle: {
			fontFamily: 'DM Sans',
			fontSize: '16px',
			fontWeight: 500,
			lineHeight: '26px',
			color: '#5E5468',
		},
		secMediumSmallLight: {
			fontFamily: 'DM Sans',
			fontSize: '14px',
			fontWeight: 400,
			lineHeight: '20px',
			color: '#5E5468',
		},
		customPrmH6Bold: {
			fontFamily: 'DM Sans',
			fontSize: '18px',
			fontWeight: 700,
			lineHeight: '30px',
			color: '#101828',
		},
		prmNormal: {
			fontFamily: 'DM Sans',
			fontSize: '14px',
			fontWeight: 500,
			lineHeight: '24px',
			color: '#101828',
		},
		customBodySec: {
			fontFamily: 'DM Sans',
			fontSize: '15px',
			fontWeight: 400,
			lineHeight: '22px',
			color: '#5E5468',
		},
		secSmall: {
			fontFamily: 'DM Sans',
			fontSize: '12px',
			fontWeight: 500,
			lineHeight: '16px',
			color: '#5E5468',
		},
		secSmallLight: {
			fontFamily: 'DM Sans',
			fontSize: '12px',
			fontWeight: 400,
			lineHeight: '20px',
			color: '#5E5468',
		},
		customPrmH5: {
			fontFamily: 'DM Sans',
			fontSize: '20px',
			fontWeight: 500,
			lineHeight: '26px',
			color: '#101828',
		},
		customPrmH4: {
			fontFamily: 'DM Sans',
			fontSize: '24px',
			fontWeight: 700,
			lineHeight: '30px',
			color: '#101828',
		},
	},
	components: {
		MuiButton: {
			defaultProps: {
				disableRipple: true,
				disableElevation: true,
			},
			styleOverrides: {
				root: {
					color: '#FFF',
					textAlign: 'center',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: '700',
					lineHeight: '18px',
					background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
					border: 'none',
					display: 'flex',
					padding: '12px 24px',
					borderRadius: '6px',
					justifyContent: 'center',
					alignItems: 'center',
					gap: '10px',
					width: 'auto',
					'&:hover': {
						border: 'none',
						background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
						color: '#FFF',
					},
					'&:active': {
						border: 'none',
						color: '#FFF',
						background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
					},
					'&:hover:before': {
						content: '""',
						position: 'absolute',
						top: 0,
						right: 0,
						bottom: 0,
						left: 0,
						zIndex: -1,
						margin: '-3px',
						borderRadius: 'inherit',
						background: 'linear-gradient(99deg, #FC73301F 2.83%, #F72A521F 97.45%)',
					},
				},
				containedPrimary: {
					color: '#FFF',
					textAlign: 'center',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: '700',
					lineHeight: '18px',
					background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
					border: 'none',
					display: 'flex',
					padding: '12px 24px',
					borderRadius: '6px',
					justifyContent: 'center',
					alignItems: 'center',
					gap: '10px',
					width: 'auto',
					'&:hover': {
						border: 'none',
						background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
						color: '#FFF',
					},
					'&:active': {
						border: 'none',
						color: '#FFF',
						background: 'linear-gradient(99deg, #FC7330 2.83%, #F72A52 97.45%)',
					},
					'&:hover:before': {
						content: '""',
						position: 'absolute',
						top: 0,
						right: 0,
						bottom: 0,
						left: 0,
						zIndex: -1,
						margin: '-3px',
						borderRadius: 'inherit',
						background: 'linear-gradient(99deg, #FC73301F 2.83%, #F72A521F 97.45%)',
					},
				},
				containedSecondary: {
					borderRadius: '8px',
					color: '#101828',
					background:
						'linear-gradient(180deg, rgba(255, 255, 255, 0.40) 0%, rgba(255, 255, 255, 0.40) 33.65%, rgba(255, 255, 255, 0.40) 65.42%, rgba(255, 255, 255, 0.40) 100%)',
					backdropFilter: 'blur(25px)',
					fontWeight: 400,
					fontSize: '12px',
					'&:hover': {
						border: 'none',
						background: 'rgba(255, 255, 255, 0.60)',
						color: '#101828',
					},
					'&:active': {
						border: 'none',
						color: '#101828',
						background: 'rgba(255, 255, 255, 0.60)',
					},
					'&:hover:before': {
						display: 'none',
					},
				},
				outlinedSecondary: {
					color: '#101828',
					textAlign: 'center',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: '700',
					lineHeight: '18px',
					background: 'transparent',
					border: '1px solid #0E1118',
					display: 'flex',
					padding: '12px 24px',
					borderRadius: '6px',
					justifyContent: 'center',
					alignItems: 'center',
					gap: '10px',
					width: 'auto',
					'&:hover': {
						border: '1px solid #0E1118',
						background:
							'linear-gradient(99deg, rgba(255, 244, 238, 0.30) 2.83%, rgba(254, 236, 240, 0.30) 97.45%)',
						color: '#101828',
					},
					'&:active': {
						border: '1px solid #0E1118',
						color: '#101828',
						background:
							'linear-gradient(99deg, rgba(255, 244, 238, 0.40) 2.83%, rgba(254, 236, 240, 0.40) 97.45%)',
					},
				},
				textPrimary: {
					color: '#FA5A3C',
					fontFamily: 'DM Sans',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: 500,
					lineHeight: '26px',
					background: 'transparent',
					height: 'auto',
					padding: '0px 16px',
					marginBlock: '8px',
					border: '1px solid transparent',
					textTransform: 'none',
					'&:hover': {
						background: 'transparent',
						color: '#FA5A3C',
						border: '1px solid #FC7330',
					},
					'&:before': {
						display: 'none',
					},
				},
			},
		},
		MuiLink: {
			styleOverrides: {
				root: {
					color: 'white',
					textDecoration: 'none',
					textTransform: 'capitalize',
					cursor: 'pointer',
				},
			},
		},
		MuiCard: {
			styleOverrides: {
				root: {
					boxShadow: ' 1px 1px 1.5px 0px rgba(0, 0, 0, 0.10)',
					border: '0.5px solid #A667DB4D',
					borderRadius: '3px',
					cursor: 'pointer',
				},
			},
			// Add other component overrides here as needed
		},
		MuiCardContent: {
			styleOverrides: {
				root: {
					borderTop: '1px solid #E4E7EC',
				},
			},
		},
		MuiTypography: {
			defaultProps: {
				variantMapping: {
					customPrmH6Bold: 'h6',
					customPrmH6: 'h6',
				},
			},
		},
		MuiRadio: {
			styleOverrides: {
				root: {
					color: '#FB6F32',
					'&.Mui-checked': {
						color: '#FB6F32',
					},
				},
			},
		},
		MuiMenuItem: {
			styleOverrides: {
				root: {
					fontSize: '14px',
					//lineHeight: '16px',
					color: '#5E5468',
					'&:not(:last-child)': {
						borderBottom: '1px solid rgba(0, 0, 0, 0.08)',
					},
					'&:last-child': {
						borderBottomLeftRadius: '8px',
						borderBottomRightRadius: '8px',
						//borderRadius: '0px 0px 8px 8px',
					},
					'&:first-of-type': {
						borderTopLeftRadius: '8px',
						borderTopRightRadius: '8px',
						//borderRadius: '8px 8px 0px 0px ',
					},
					// Default state styles here
					'&:hover': {
						background: '#F2E8F9', // The color you want for hover
					},
					// If you also want to change the selected item color:
					'&.Mui-selected': {
						background: 'linear-gradient(0deg, #F2E8F9, #E4E8EE)', // The color for selected item
						'&.Mui-focusVisible': {
							background: 'linear-gradient(0deg, #F2E8F9, #E4E8EE)', // Replace with your desired color
						},
						'&:hover': {
							background: 'linear-gradient(0deg, #F2E8F9, #E4E8EE)', // The color for selected item on hover
						},
					},
				},
			},
		},
		MuiMenu: {
			styleOverrides: {
				list: {
					paddingBlock: '0px',
					borderRadius: '8px',
					background: '#F2F5F8',
					maxHeight: '60vh',
					overflowY: 'auto',
				},
				paper: {
					borderRadius: '8px',
					boxShadow: 'none',
					overflow: 'visible',
					'&:before': {
						content: '""',
						position: 'absolute',
						top: 0,
						right: 0,
						bottom: 0,
						left: 0,
						zIndex: -1,
						margin: '-1px',
						borderRadius: 'inherit',
						background: 'linear-gradient(to right, #cdbedd, #ffffff)',
					},
				},
			},
		},
		MuiInputAdornment: {
			styleOverrides: {
				root: {
					cursor: 'pointer',
				},
			},
		},
		MuiInput: {
			styleOverrides: {
				underline: {
					'&:before': {
						display: 'none',
					},
				},
			},
		},
		MuiInputBase: {
			styleOverrides: {
				root: {
					background: 'rgba(255, 255, 255, 0.6)',
					borderRadius: '8px',
					borderColor: 'transparent',
				},
			},
		},
		MuiOutlinedInput: {
			styleOverrides: {
				root: {
					borderRadius: '8px',
					fontWeight: 400,
					fontSize: '16px',
					fontFamily: 'DM Sans',
					'& .MuiOutlinedInput-notchedOutline': {
						border: '1px solid transparent',
						borderLeft: '1px solid white',
						borderTop: '1px solid white',
					},
					'&:hover .MuiOutlinedInput-notchedOutline': {
						border: '1px solid transparent',
					},
					'&.Mui-focused .MuiOutlinedInput-notchedOutline': {
						border: '2px solid #A264e0',
					},
				},
				sizeSmall: {
					'&.Mui-focused .MuiOutlinedInput-notchedOutline': {
						border: '1px solid #A264e0',
					},
				},
			},
		},
		MuiSelect: {
			styleOverrides: {
				root: {
					minWidth: '110px',
					borderRadius: '8px',
					border: 'none !important',
					backgroundColor: 'rgba(255, 255, 255, 0.20) !important',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: 500,
					lineHeight: '16px',
					height: '43px',
					verticalAlign: 'middle',
					minHeight: '43px',
					'&:hover': {
						backgroundColor: 'rgba(255, 255, 255, 0.60) !important',
					},
					'&.Mui-focused': {
						backgroundColor: 'rgba(255, 255, 255, 0.60) !important',
					},
					'& .MuiInputBase-root': {
						background: 'none !important',
						border: 'none',
					},
					'& .MuiOutlinedInput-root': {
						background: 'none !important',
					},
					'& .MuiOutlinedInput-notchedOutline': {
						border: 'none',
					},
					'&:after': {
						display: 'none',
					},
				},

				icon: {
					fill: 'none',
					right: 16,
					fontSize: 20,
				},
				select: {
					padding: '8px 44px 8px 16px !important',
					border: 'none !important',
					minHeight: 'auto',
				},
			},
			defaultProps: {
				IconComponent: ChevronDownIcon,
			},
		},

		MuiListItem: {
			styleOverrides: {
				root: {
					width: '100%',
					borderRadius: '6px',
					background: '#EFF1F4',
					padding: '15px 10px',
					marginBottom: '5px',
					color: '#133447',
					fontSize: '14px',
					fontWeight: 400,
					fontFamily: "'DM Sans', 'Source Sans 3', sans-serif",
				},
			},
		},
		MuiTab: {
			styleOverrides: {
				root: {
					paddingLeft: 0,
					paddingRight: 0,
					marginRight: '24px',
					paddingBlock: '8px',
					minWidth: 'auto',
					color: '#5E5468',
					textTransform: 'capitalize',
					fontFamily: 'DM Sans',
					fontSize: '16px',
					fontStyle: 'normal',
					fontWeight: 500,
					lineHeight: '26px',
					'&.Mui-selected': {
						color: '#101828',
					},
				},
			},
		},
		MuiTabs: {
			styleOverrides: {
				root: {},
				indicator: {
					background: 'linear-gradient(to right, #FB6238, #F8374C)',
					height: 2,
				},
			},
		},
		MuiDataGrid: {
			styleOverrides: {
				root: {
					backgroundColor: 'rgba(255, 255, 255, 0.60)',
					borderRadius: '8px',
					boxShadow: 'none',
					border: 'none',
					overflow: 'clip',
				},
				columnHeaders: {
					minHeight: '48px !important',
					maxHeight: '48px !important',
					backgroundColor: '#fff',
				},
				columnHeader: {
					color: '#101828',
					fontFamily: 'DM Sans',
					fontSize: '12px',
					fontStyle: 'normal',
					fontWeight: 600,
					lineHeight: '16px',
					letterSpacing: '0.36px',
					textTransform: 'uppercase',
					minHeight: '48px !important',
					maxHeight: '48px !important',
				},
				columnHeaderTitle: {
					fontWeight: 600,
					whiteSpace: 'break-spaces',
					maxHeight: '32px',
					MozLineClamp: 3,
					WebkitBoxOrient: 'vertical',
					WebkitLineClamp: 3,
					WebkitLineBreak: 'anywhere',
				},
				cell: {
					color: '#5E5468',
					fontFamily: 'DM Sans',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: 400,
					lineHeight: '26px',
					padding: '12px',
					minHeight: '50px !important',
					maxHeight: '100% !important',
				},
				row: {
					minHeight: '50px !important',
					maxHeight: '100% !important',
				},
				withBorderColor: {
					borderColor: '#DBD7EE',
				},
				footerContainer: {
					minHeight: '50px !important',
					maxHeight: '50px !important',
				},
			},
		},
		MuiTablePagination: {
			styleOverrides: {
				root: {},
				displayedRows: {
					color: '#101828',
					fontFamily: 'DM Sans',
					fontSize: '12px',
					fontStyle: 'normal',
					fontWeight: '500',
					lineHeight: '16px',
				},
			},
		},
		MuiToolbar: {
			styleOverrides: {
				root: {
					'&.MuiTablePagination-toolbar': {
						minHeight: '50px !important',
						maxHeight: '50px !important',
					},
				},
			},
		},
		MuiTableContainer: {
			styleOverrides: {
				root: {
					backgroundColor: 'rgba(255, 255, 255, 0.60)',
					borderRadius: '8px',
					boxShadow: 'none',
				},
			},
		},
		MuiTableCell: {
			styleOverrides: {
				root: {
					color: '#5E5468',
					fontFamily: 'DM Sans',
					fontSize: '14px',
					fontStyle: 'normal',
					fontWeight: 400,
					lineHeight: '26px',
					padding: '12px',
				},
				head: {
					color: '#101828',
					fontFamily: 'DM Sans',
					fontSize: '12px',
					fontStyle: 'normal',
					fontWeight: 500,
					lineHeight: '16px',
					letterSpacing: '0.36px',
					textTransform: 'uppercase',
				},
			},
		},
		MuiAutocomplete: {
			styleOverrides: {
				root: {
					'& .MuiAutocomplete-popupIndicator': {
						padding: '4px',
						width: '28px',
						height: '28px',
					},
				},
				listbox: {
					borderRadius: '8px',
					padding: '0px',
					backgroundColor: '#f2f5f8',
				},
				option: {
					paddingBlock: '12px !important',
					paddingInline: '12px',
					fontWeight: 400,
					fontSize: '14px',
					lineHeight: '16px',
					color: '#5e5468',
				},
				paper: {
					borderRadius: '8px',
				},
				input: {
					'&::placeholder': {
						color: '#5e5468',
						fontWeight: 400,
						fontSize: '16px',
						lineHeight: '24px',
					},
				},
			},
			defaultProps: {
				popupIcon: <DownChevronSmall sx={{ fill: 'none', fontSize: '12px' }} />,
			},
		},
	},
});
