import { Link } from 'react-router-dom'
import { Home, AlertTriangle } from 'lucide-react'

export default function NotFoundPage() {
    return (
        <div className="min-h-[60vh] flex items-center justify-center animate-fade-in">
            <div className="text-center">
                <div className="h-24 w-24 rounded-full bg-yellow-100 flex items-center justify-center mx-auto mb-6">
                    <AlertTriangle className="h-12 w-12 text-yellow-600" />
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
                <p className="text-xl text-gray-600 mb-8">Page not found</p>
                <p className="text-gray-500 mb-8 max-w-md">
                    The page you're looking for doesn't exist or has been moved.
                </p>
                <Link to="/" className="btn-primary gap-2">
                    <Home className="h-5 w-5" />
                    Back to Home
                </Link>
            </div>
        </div>
    )
}
