import { Link } from 'react-router-dom'
import { PlusCircle, Search, Filter, Eye, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { useState } from 'react'

// Mock data for demonstration
const mockApplications = [
    {
        id: '1',
        applicantName: 'John Doe',
        loanAmount: 50000,
        loanType: 'Personal Loan',
        status: 'pending',
        createdAt: '2026-01-03',
    },
    {
        id: '2',
        applicantName: 'Jane Smith',
        loanAmount: 250000,
        loanType: 'Mortgage',
        status: 'approved',
        createdAt: '2026-01-02',
    },
    {
        id: '3',
        applicantName: 'Bob Johnson',
        loanAmount: 15000,
        loanType: 'Auto Loan',
        status: 'rejected',
        createdAt: '2026-01-01',
    },
    {
        id: '4',
        applicantName: 'Alice Williams',
        loanAmount: 75000,
        loanType: 'Business Loan',
        status: 'under_review',
        createdAt: '2025-12-31',
    },
]

const statusConfig = {
    pending: { label: 'Pending', icon: Clock, className: 'badge-warning' },
    approved: { label: 'Approved', icon: CheckCircle, className: 'badge-success' },
    rejected: { label: 'Rejected', icon: XCircle, className: 'badge-danger' },
    under_review: { label: 'Under Review', icon: AlertCircle, className: 'badge-info' },
}

export default function ApplicationsPage() {
    const [searchQuery, setSearchQuery] = useState('')
    const [statusFilter, setStatusFilter] = useState<string>('all')

    const filteredApplications = mockApplications.filter((app) => {
        const matchesSearch = app.applicantName.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesStatus = statusFilter === 'all' || app.status === statusFilter
        return matchesSearch && matchesStatus
    })

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Loan Applications</h1>
                    <p className="text-gray-600 mt-1">Manage and track all loan applications</p>
                </div>
                <Link to="/applications/new" className="btn-primary gap-2">
                    <PlusCircle className="h-5 w-5" />
                    New Application
                </Link>
            </div>

            {/* Filters */}
            <div className="card mb-6">
                <div className="card-body">
                    <div className="flex flex-col sm:flex-row gap-4">
                        <div className="flex-1 relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search by applicant name..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="input pl-10"
                            />
                        </div>
                        <div className="relative">
                            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="input pl-10 pr-8 appearance-none cursor-pointer min-w-[180px]"
                            >
                                <option value="all">All Statuses</option>
                                <option value="pending">Pending</option>
                                <option value="under_review">Under Review</option>
                                <option value="approved">Approved</option>
                                <option value="rejected">Rejected</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            {/* Applications Table */}
            <div className="card overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Applicant
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Loan Type
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Amount
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Status
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Date
                                </th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {filteredApplications.map((application) => {
                                const status = statusConfig[application.status as keyof typeof statusConfig]
                                const StatusIcon = status.icon
                                return (
                                    <tr key={application.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="font-medium text-gray-900">{application.applicantName}</div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                                            {application.loanType}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-900 font-medium">
                                            ${application.loanAmount.toLocaleString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={status.className}>
                                                <StatusIcon className="h-3.5 w-3.5 mr-1" />
                                                {status.label}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                                            {application.createdAt}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right">
                                            <Link
                                                to={`/applications/${application.id}`}
                                                className="inline-flex items-center gap-1 text-primary-600 hover:text-primary-700 font-medium text-sm"
                                            >
                                                <Eye className="h-4 w-4" />
                                                View
                                            </Link>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </div>

                {filteredApplications.length === 0 && (
                    <div className="text-center py-12">
                        <p className="text-gray-500">No applications found matching your criteria.</p>
                    </div>
                )}
            </div>
        </div>
    )
}
