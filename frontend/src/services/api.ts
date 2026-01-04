import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor for handling errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

// API functions for loan applications
export const applicationApi = {
    getAll: () => api.get('/applications'),
    getById: (id: string) => api.get(`/applications/${id}`),
    create: (data: FormData) => api.post('/applications', data, {
        headers: { 'Content-Type': 'multipart/form-data' },
    }),
    update: (id: string, data: unknown) => api.patch(`/applications/${id}`, data),
    delete: (id: string) => api.delete(`/applications/${id}`),
}

// API functions for documents
export const documentApi = {
    upload: (applicationId: string, file: File) => {
        const formData = new FormData()
        formData.append('file', file)
        return api.post(`/applications/${applicationId}/documents`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
    },
    getByApplication: (applicationId: string) =>
        api.get(`/applications/${applicationId}/documents`),
    delete: (documentId: string) => api.delete(`/documents/${documentId}`),
}

export default api
