import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ApplicationsPage from './pages/ApplicationsPage'
import NewApplicationPage from './pages/NewApplicationPage'
import ApplicationDetailPage from './pages/ApplicationDetailPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path="applications" element={<ApplicationsPage />} />
                <Route path="applications/new" element={<NewApplicationPage />} />
                <Route path="applications/:id" element={<ApplicationDetailPage />} />
                <Route path="*" element={<NotFoundPage />} />
            </Route>
        </Routes>
    )
}

export default App
