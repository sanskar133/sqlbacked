import { ReactNode } from 'react';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog, { DialogProps } from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
	'& .MuiDialog-paper': { borderRadius: '8px' },
	'& .MuiDialogContent-root': {
		padding: theme.spacing(2),
	},
	'& .MuiDialogActions-root': {
		padding: theme.spacing(1),
	},
}));

interface GenericModalProps {
	title: string;
	children: ReactNode;
	open: boolean;
	handleSubmit: () => void;
	handleClose: () => void;
	btnText: string;
	disabled?: boolean;
	maxWidth?: DialogProps['maxWidth'];
	fullWidth: boolean;
	popupType?: string;
}

const GenericModal = ({
	title,
	open = false,
	handleSubmit,
	handleClose,
	btnText = 'Submit Changes',
	children,
	disabled = false,
	fullWidth = false,
	maxWidth = 'sm',
	popupType,
}: GenericModalProps) => {
	return (
		<BootstrapDialog
			onClose={popupType === 'POPUP_RED' ? () => {} : handleClose}
			aria-labelledby="customized-dialog-title"
			open={open}
			fullWidth={fullWidth}
			maxWidth={maxWidth}
			disableEscapeKeyDown={popupType === 'POPUP_RED'}
		>
			<DialogTitle
				sx={
					popupType === undefined
						? {
								m: 0,
								p: 2,
								fontSize: '20px',
								textTransform: 'uppercase',
								borderBottom: '1px solid #E4E7EC',
							}
						: {
								m: 0,
								p: 2,
								fontSize: '20px',
								textTransform: 'uppercase',
								borderBottom: '1px solid #E4E7EC',
								backgroundColor:
									popupType === 'POPUP_GREEN' ? '#6DDE6A' : '#F77C7C',
								color: 'white',
							}
				}
				id="customized-dialog-title"
			>
				{title}
			</DialogTitle>
			<IconButton
				aria-label="close"
				onClick={handleClose}
				sx={{
					display: popupType === 'POPUP_RED' ? 'none' : 'inline',
					position: 'absolute',
					right: 8,
					top: 8,
					color: (theme) => (popupType === undefined ? theme.palette.grey[500] : 'white'),
				}}
			>
				<CloseIcon />
			</IconButton>
			<DialogContent>{children}</DialogContent>
			{btnText === '' ? null : (
				<DialogActions sx={{ borderTop: '1px solid #E4E7EC' }}>
					<Button variant="contained" onClick={handleSubmit} disabled={disabled}>
						{btnText}
					</Button>
				</DialogActions>
			)}
		</BootstrapDialog>
	);
};

export default GenericModal;
