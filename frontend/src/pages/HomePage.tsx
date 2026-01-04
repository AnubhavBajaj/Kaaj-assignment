import { Link } from 'react-router-dom'
import { ArrowRight, FileText, Shield, Clock, TrendingUp } from 'lucide-react'

const features = [
    {
        name: 'Fast Processing',
        description: 'Get your loan application processed within 24-48 hours.',
        icon: Clock,
    },
    {
        name: 'Secure & Private',
        description: 'Your data is encrypted and protected with enterprise-grade security.',
        icon: Shield,
    },
    {
        name: 'Smart Underwriting',
        description: 'AI-powered risk assessment for faster and more accurate decisions.',
        icon: TrendingUp,
    },
    {
        name: 'Document Management',
        description: 'Easily upload and manage all your loan documents in one place.',
        icon: FileText,
    },
]

export default function HomePage() {
    return (
        <div className="animate-fade-in">
            {/* Hero Section */}
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 via-primary-700 to-accent-700 text-white mb-12">
                <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48cGF0aCBkPSJNMzYgMzRjMC0yLjIwOSAxLjc5MS00IDQtNHM0IDEuNzkxIDQgNC0xLjc5MSA0LTQgNC00LTEuNzkxLTQtNHptMC0xNmMwLTIuMjA5IDEuNzkxLTQgNC00czQgMS43OTEgNCA0LTEuNzkxIDQtNCA0LTQtMS43OTEtNC00em0tMTYgMTZjMC0yLjIwOSAxLjc5MS00IDQtNHM0IDEuNzkxIDQgNC0xLjc5MSA0LTQgNC00LTEuNzkxLTQtNHptMC0xNmMwLTIuMjA5IDEuNzkxLTQgNC00czQgMS43OTEgNCA0LTEuNzkxIDQtNCA0LTQtMS43OTEtNC00eiIvPjwvZz48L2c+PC9zdmc+')] opacity-20"></div>
                <div className="relative px-8 py-16 sm:px-16 sm:py-24">
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
                        Smart Loan
                        <span className="block">Underwriting</span>
                    </h1>
                    <p className="text-lg sm:text-xl text-primary-100 max-w-2xl mb-8">
                        Streamline your loan application process with our AI-powered underwriting platform.
                        Fast, secure, and reliable lending decisions.
                    </p>
                    <div className="flex flex-wrap gap-4">
                        <Link
                            to="/applications/new"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-white text-primary-700 font-semibold rounded-xl hover:bg-primary-50 transition-all duration-200 shadow-lg hover:shadow-xl"
                        >
                            Apply Now
                            <ArrowRight className="h-5 w-5" />
                        </Link>
                        <Link
                            to="/applications"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-primary-500/20 text-white font-semibold rounded-xl hover:bg-primary-500/30 transition-all duration-200 border border-white/20"
                        >
                            View Applications
                        </Link>
                    </div>
                </div>
            </div>

            {/* Features Section */}
            <div className="mb-12">
                <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-8 text-center">
                    Why Choose <span className="text-gradient">LoanFlow</span>?
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {features.map((feature, index) => (
                        <div
                            key={feature.name}
                            className="card p-6 hover:shadow-lg transition-all duration-300 animate-slide-up"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary-100 to-accent-100 flex items-center justify-center mb-4">
                                <feature.icon className="h-6 w-6 text-primary-600" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.name}</h3>
                            <p className="text-gray-600 text-sm">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Stats Section */}
            <div className="card p-8">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
                    <div>
                        <p className="text-4xl font-bold text-gradient">10K+</p>
                        <p className="text-gray-600 mt-1">Applications Processed</p>
                    </div>
                    <div>
                        <p className="text-4xl font-bold text-gradient">24h</p>
                        <p className="text-gray-600 mt-1">Average Processing Time</p>
                    </div>
                    <div>
                        <p className="text-4xl font-bold text-gradient">98%</p>
                        <p className="text-gray-600 mt-1">Customer Satisfaction</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
