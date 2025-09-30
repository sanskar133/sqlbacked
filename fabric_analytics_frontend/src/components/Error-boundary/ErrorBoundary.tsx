import React, { ErrorInfo, ReactNode } from 'react';
import ErrorFallback from './ErrorFallback';

interface CustomErrorBoundaryProps {
	children: ReactNode;
}

interface CustomErrorBoundaryState {
	hasError: boolean;
}

class CustomErrorBoundary extends React.Component<
	CustomErrorBoundaryProps,
	CustomErrorBoundaryState
> {
	constructor(props: CustomErrorBoundaryProps) {
		super(props);
		this.state = { hasError: false };
	}

	static getDerivedStateFromError(_: Error): CustomErrorBoundaryState {
		return { hasError: true };
	}

	componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
		console.error('Error caught by custom error boundary:', error, errorInfo);
		// You can also log the error to an error reporting service
	}

	render(): ReactNode {
		if (this.state.hasError) {
			return <ErrorFallback />;
		}
		return this.props.children;
	}
}

export default CustomErrorBoundary;
