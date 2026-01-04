import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Upload, ArrowLeft, Send } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

const applicationSchema = z.object({
    firstName: z.string().min(2, 'First name must be at least 2 characters'),
    lastName: z.string().min(2, 'Last name must be at least 2 characters'),
    email: z.string().email('Please enter a valid email address'),
    phone: z.string().min(10, 'Please enter a valid phone number'),
    loanType: z.enum(['personal', 'mortgage', 'auto', 'business'], {
        required_error: 'Please select a loan type',
    }),
    loanAmount: z.number().min(1000, 'Minimum loan amount is $1,000').max(1000000, 'Maximum loan amount is $1,000,000'),
    loanPurpose: z.string().min(10, 'Please describe the purpose of the loan'),
    annualIncome: z.number().min(0, 'Annual income must be a positive number'),
    employmentStatus: z.enum(['employed', 'self_employed', 'unemployed', 'retired'], {
        required_error: 'Please select your employment status',
    }),
    employerName: z.string().optional(),
})

type ApplicationFormData = z.infer<typeof applicationSchema>

export default function NewApplicationPage() {
    const navigate = useNavigate()
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([])

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<ApplicationFormData>({
        resolver: zodResolver(applicationSchema),
    })

    const onSubmit = async (data: ApplicationFormData) => {
        setIsSubmitting(true)
        // Simulate API call
        console.log('Form data:', data)
        console.log('Uploaded files:', uploadedFiles)

        await new Promise((resolve) => setTimeout(resolve, 1500))
        setIsSubmitting(false)
        navigate('/applications')
    }

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setUploadedFiles([...uploadedFiles, ...Array.from(e.target.files)])
        }
    }

    const removeFile = (index: number) => {
        setUploadedFiles(uploadedFiles.filter((_, i) => i !== index))
    }

    return (
        <div className="animate-fade-in max-w-3xl mx-auto">
            {/* Header */}
            <div className="mb-8">
                <Link
                    to="/applications"
                    className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
                >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Applications
                </Link>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">New Loan Application</h1>
                <p className="text-gray-600 mt-1">Fill out the form below to submit a new loan application</p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
                {/* Personal Information */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="text-lg font-semibold text-gray-900">Personal Information</h2>
                    </div>
                    <div className="card-body space-y-4">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label className="label">First Name</label>
                                <input
                                    {...register('firstName')}
                                    className={errors.firstName ? 'input-error' : 'input'}
                                    placeholder="John"
                                />
                                {errors.firstName && (
                                    <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
                                )}
                            </div>
                            <div>
                                <label className="label">Last Name</label>
                                <input
                                    {...register('lastName')}
                                    className={errors.lastName ? 'input-error' : 'input'}
                                    placeholder="Doe"
                                />
                                {errors.lastName && (
                                    <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
                                )}
                            </div>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label className="label">Email</label>
                                <input
                                    {...register('email')}
                                    type="email"
                                    className={errors.email ? 'input-error' : 'input'}
                                    placeholder="john@example.com"
                                />
                                {errors.email && (
                                    <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
                                )}
                            </div>
                            <div>
                                <label className="label">Phone Number</label>
                                <input
                                    {...register('phone')}
                                    type="tel"
                                    className={errors.phone ? 'input-error' : 'input'}
                                    placeholder="+1 (555) 000-0000"
                                />
                                {errors.phone && (
                                    <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Loan Details */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="text-lg font-semibold text-gray-900">Loan Details</h2>
                    </div>
                    <div className="card-body space-y-4">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label className="label">Loan Type</label>
                                <select
                                    {...register('loanType')}
                                    className={errors.loanType ? 'input-error' : 'input'}
                                >
                                    <option value="">Select loan type</option>
                                    <option value="personal">Personal Loan</option>
                                    <option value="mortgage">Mortgage</option>
                                    <option value="auto">Auto Loan</option>
                                    <option value="business">Business Loan</option>
                                </select>
                                {errors.loanType && (
                                    <p className="text-red-500 text-sm mt-1">{errors.loanType.message}</p>
                                )}
                            </div>
                            <div>
                                <label className="label">Loan Amount ($)</label>
                                <input
                                    {...register('loanAmount', { valueAsNumber: true })}
                                    type="number"
                                    className={errors.loanAmount ? 'input-error' : 'input'}
                                    placeholder="50000"
                                />
                                {errors.loanAmount && (
                                    <p className="text-red-500 text-sm mt-1">{errors.loanAmount.message}</p>
                                )}
                            </div>
                        </div>
                        <div>
                            <label className="label">Purpose of Loan</label>
                            <textarea
                                {...register('loanPurpose')}
                                rows={3}
                                className={errors.loanPurpose ? 'input-error' : 'input'}
                                placeholder="Describe how you plan to use the loan..."
                            />
                            {errors.loanPurpose && (
                                <p className="text-red-500 text-sm mt-1">{errors.loanPurpose.message}</p>
                            )}
                        </div>
                    </div>
                </div>

                {/* Employment Information */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="text-lg font-semibold text-gray-900">Employment Information</h2>
                    </div>
                    <div className="card-body space-y-4">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label className="label">Employment Status</label>
                                <select
                                    {...register('employmentStatus')}
                                    className={errors.employmentStatus ? 'input-error' : 'input'}
                                >
                                    <option value="">Select status</option>
                                    <option value="employed">Employed</option>
                                    <option value="self_employed">Self-Employed</option>
                                    <option value="unemployed">Unemployed</option>
                                    <option value="retired">Retired</option>
                                </select>
                                {errors.employmentStatus && (
                                    <p className="text-red-500 text-sm mt-1">{errors.employmentStatus.message}</p>
                                )}
                            </div>
                            <div>
                                <label className="label">Annual Income ($)</label>
                                <input
                                    {...register('annualIncome', { valueAsNumber: true })}
                                    type="number"
                                    className={errors.annualIncome ? 'input-error' : 'input'}
                                    placeholder="75000"
                                />
                                {errors.annualIncome && (
                                    <p className="text-red-500 text-sm mt-1">{errors.annualIncome.message}</p>
                                )}
                            </div>
                        </div>
                        <div>
                            <label className="label">Employer Name (Optional)</label>
                            <input
                                {...register('employerName')}
                                className="input"
                                placeholder="Company Inc."
                            />
                        </div>
                    </div>
                </div>

                {/* Document Upload */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="text-lg font-semibold text-gray-900">Supporting Documents</h2>
                    </div>
                    <div className="card-body">
                        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-primary-400 transition-colors">
                            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <p className="text-gray-600 mb-2">Drag and drop files here, or click to browse</p>
                            <p className="text-sm text-gray-500 mb-4">PDF, JPG, PNG up to 10MB each</p>
                            <label className="btn-secondary cursor-pointer">
                                <input
                                    type="file"
                                    className="hidden"
                                    multiple
                                    accept=".pdf,.jpg,.jpeg,.png"
                                    onChange={handleFileUpload}
                                />
                                Choose Files
                            </label>
                        </div>

                        {uploadedFiles.length > 0 && (
                            <div className="mt-4 space-y-2">
                                {uploadedFiles.map((file, index) => (
                                    <div
                                        key={index}
                                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                                    >
                                        <span className="text-sm text-gray-700 truncate">{file.name}</span>
                                        <button
                                            type="button"
                                            onClick={() => removeFile(index)}
                                            className="text-red-500 hover:text-red-700 text-sm font-medium"
                                        >
                                            Remove
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* Submit Button */}
                <div className="flex justify-end">
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="btn-primary gap-2 px-8"
                    >
                        {isSubmitting ? (
                            <>
                                <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                Submitting...
                            </>
                        ) : (
                            <>
                                <Send className="h-5 w-5" />
                                Submit Application
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    )
}
