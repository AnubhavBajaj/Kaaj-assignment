// Loan Application Types

export type LoanType = 'personal' | 'mortgage' | 'auto' | 'business'

export type EmploymentStatus = 'employed' | 'self_employed' | 'unemployed' | 'retired'

export type ApplicationStatus = 'pending' | 'under_review' | 'approved' | 'rejected'

export interface LoanApplication {
    id: string
    firstName: string
    lastName: string
    email: string
    phone: string
    loanType: LoanType
    loanAmount: number
    loanPurpose: string
    annualIncome: number
    employmentStatus: EmploymentStatus
    employerName?: string
    status: ApplicationStatus
    createdAt: string
    updatedAt: string
}

export interface LoanApplicationCreate {
    firstName: string
    lastName: string
    email: string
    phone: string
    loanType: LoanType
    loanAmount: number
    loanPurpose: string
    annualIncome: number
    employmentStatus: EmploymentStatus
    employerName?: string
}

export interface Document {
    id: string
    applicationId: string
    filename: string
    contentType: string
    size: number
    uploadedAt: string
}

export interface TimelineEvent {
    date: string
    event: string
    completed: boolean
}

export interface ApplicationDetail extends LoanApplication {
    documents: Document[]
    timeline: TimelineEvent[]
}

// API Response Types
export interface ApiResponse<T> {
    data: T
    message?: string
}

export interface PaginatedResponse<T> {
    items: T[]
    total: number
    page: number
    pageSize: number
    hasMore: boolean
}

export interface ApiError {
    message: string
    code?: string
    details?: Record<string, string[]>
}
