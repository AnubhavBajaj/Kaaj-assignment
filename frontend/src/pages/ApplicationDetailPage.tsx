import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, FileText, User, Briefcase, DollarSign, Calendar, Clock, CheckCircle } from 'lucide-react'

// Mock data for demonstration
const mockApplication = {
    id: '1',
    applicantName: 'John Doe',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    loanAmount: 50000,
    loanType: 'Personal Loan',
    loanPurpose: 'Home renovation and debt consolidation. Planning to upgrade the kitchen and bathroom, and pay off existing credit card debt.',
    status: 'under_review',
    annualIncome: 85000,
    employmentStatus: 'Employed',
    employerName: 'Tech Solutions Inc.',
    createdAt: '2026-01-03',
    documents: [
        { name: 'pay_stubs.pdf', size: '245 KB', uploadedAt: '2026-01-03' },
        { name: 'bank_statements.pdf', size: '1.2 MB', uploadedAt: '2026-01-03' },
        { name: 'tax_returns_2025.pdf', size: '890 KB', uploadedAt: '2026-01-03' },
    ],
    timeline: [
        { date: '2026-01-03', event: 'Application submitted', completed: true },
        { date: '2026-01-04', event: 'Documents verified', completed: true },
        { date: '2026-01-04', event: 'Credit check initiated', completed: true },
        { date: 'Pending', event: 'Underwriting review', completed: false },
        { date: 'Pending', event: 'Final decision', completed: false },
    ],
}

export default function ApplicationDetailPage() {
    const { id } = useParams()
    const application = mockApplication // In real app, fetch by id

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="mb-8">
                <Link
                    to="/applications"
                    className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
                >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Applications
                </Link>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                            Application #{id}
                        </h1>
                        <p className="text-gray-600 mt-1">Submitted on {application.createdAt}</p>
                    </div>
                    <span className="badge-info text-sm px-4 py-2">
                        <Clock className="h-4 w-4 mr-2" />
                        Under Review
                    </span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Applicant Information */}
                    <div className="card">
                        <div className="card-header flex items-center gap-2">
                            <User className="h-5 w-5 text-primary-600" />
                            <h2 className="text-lg font-semibold text-gray-900">Applicant Information</h2>
                        </div>
                        <div className="card-body">
                            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
                                <div>
                                    <dt className="text-sm text-gray-500">Full Name</dt>
                                    <dd className="text-gray-900 font-medium">{application.firstName} {application.lastName}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-gray-500">Email</dt>
                                    <dd className="text-gray-900">{application.email}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-gray-500">Phone</dt>
                                    <dd className="text-gray-900">{application.phone}</dd>
                                </div>
                            </dl>
                        </div>
                    </div>

                    {/* Loan Details */}
                    <div className="card">
                        <div className="card-header flex items-center gap-2">
                            <DollarSign className="h-5 w-5 text-primary-600" />
                            <h2 className="text-lg font-semibold text-gray-900">Loan Details</h2>
                        </div>
                        <div className="card-body">
                            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
                                <div>
                                    <dt className="text-sm text-gray-500">Loan Type</dt>
                                    <dd className="text-gray-900 font-medium">{application.loanType}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-gray-500">Amount Requested</dt>
                                    <dd className="text-2xl font-bold text-gradient">${application.loanAmount.toLocaleString()}</dd>
                                </div>
                                <div className="sm:col-span-2">
                                    <dt className="text-sm text-gray-500">Purpose</dt>
                                    <dd className="text-gray-900 mt-1">{application.loanPurpose}</dd>
                                </div>
                            </dl>
                        </div>
                    </div>

                    {/* Employment Information */}
                    <div className="card">
                        <div className="card-header flex items-center gap-2">
                            <Briefcase className="h-5 w-5 text-primary-600" />
                            <h2 className="text-lg font-semibold text-gray-900">Employment Information</h2>
                        </div>
                        <div className="card-body">
                            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
                                <div>
                                    <dt className="text-sm text-gray-500">Employment Status</dt>
                                    <dd className="text-gray-900 font-medium">{application.employmentStatus}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-gray-500">Employer</dt>
                                    <dd className="text-gray-900">{application.employerName}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-gray-500">Annual Income</dt>
                                    <dd className="text-gray-900 font-medium">${application.annualIncome.toLocaleString()}</dd>
                                </div>
                            </dl>
                        </div>
                    </div>

                    {/* Documents */}
                    <div className="card">
                        <div className="card-header flex items-center gap-2">
                            <FileText className="h-5 w-5 text-primary-600" />
                            <h2 className="text-lg font-semibold text-gray-900">Uploaded Documents</h2>
                        </div>
                        <div className="card-body">
                            <div className="space-y-3">
                                {application.documents.map((doc, index) => (
                                    <div
                                        key={index}
                                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="h-10 w-10 rounded-lg bg-primary-100 flex items-center justify-center">
                                                <FileText className="h-5 w-5 text-primary-600" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">{doc.name}</p>
                                                <p className="text-sm text-gray-500">{doc.size} • {doc.uploadedAt}</p>
                                            </div>
                                        </div>
                                        <button className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                                            View
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Sidebar - Timeline */}
                <div className="lg:col-span-1">
                    <div className="card sticky top-24">
                        <div className="card-header flex items-center gap-2">
                            <Calendar className="h-5 w-5 text-primary-600" />
                            <h2 className="text-lg font-semibold text-gray-900">Application Timeline</h2>
                        </div>
                        <div className="card-body">
                            <ol className="relative border-l border-gray-200 ml-3 space-y-6">
                                {application.timeline.map((item, index) => (
                                    <li key={index} className="ml-6">
                                        <span
                                            className={`absolute flex items-center justify-center w-6 h-6 rounded-full -left-3 ${item.completed
                                                    ? 'bg-green-100 ring-4 ring-white'
                                                    : 'bg-gray-100 ring-4 ring-white'
                                                }`}
                                        >
                                            {item.completed ? (
                                                <CheckCircle className="h-4 w-4 text-green-600" />
                                            ) : (
                                                <div className="h-2 w-2 bg-gray-400 rounded-full" />
                                            )}
                                        </span>
                                        <div>
                                            <p className={`font-medium ${item.completed ? 'text-gray-900' : 'text-gray-500'}`}>
                                                {item.event}
                                            </p>
                                            <p className="text-sm text-gray-500">{item.date}</p>
                                        </div>
                                    </li>
                                ))}
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
