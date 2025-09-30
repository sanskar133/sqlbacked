import { Route, Routes } from 'react-router-dom';
import { Suspense, lazy } from 'react';
import AppMainLoader from '../components/shared/AppMainLoader';
import { routes } from './routes';
const ErrorBoundary = lazy(() => import('../components/Error-boundary/ErrorBoundary'));
const PrivateLayoutComponent = lazy(() => import('../components/shared/Layout/PrivateLayout'));
const PageNotfound = lazy(() => import('../pages/PageNotFound'));
const HomePageChat = lazy(() => import('../pages/HomePageChat'));
const EcomChatPage = lazy(() => import('../pages/EcomChatPage'));

const Index = () => {
	return (
		<>
			<Suspense fallback={<AppMainLoader />}>
				<ErrorBoundary>
					<Routes>
						<Route path={routes.home} element={<HomePageChat />} />
						<Route
							path={routes.chat}
							element={
								<PrivateLayoutComponent>
									<EcomChatPage />
								</PrivateLayoutComponent>
							}
						/>
						<Route path={routes.pageNotFound} element={<PageNotfound />} />
					</Routes>
				</ErrorBoundary>
			</Suspense>
		</>
	);
};

export default Index;
