import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

let currentMerchantId = null;

export const setMerchantId = (merchantId) => {
    currentMerchantId = merchantId;
};

export const getMerchantId = () => currentMerchantId;

apiClient.interceptors.request.use(
    (config) => {
        if (currentMerchantId) {
            config.headers['X-Merchant-ID'] = currentMerchantId;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 404) {
            console.warn('🚨 Resource not found - may belong to different merchant');
        }
        return Promise.reject(error);
    }
);

export const fetchTransactions = async (page = 1, status = null) => {
    const params = { page };
    if (status) params.status = status;
    const response = await apiClient.get('merchants/transactions/', { params });
    return response.data;
};

export const fetchAnalyticsSummary = async () => {
    const response = await apiClient.get('analytics/summary/');
    return response.data;
};

export const requestExport = async (format = 'csv', dateRange = null) => {
    const payload = { format };
    if (dateRange) payload.date_range = dateRange;
    const response = await apiClient.post('analytics/export/', payload);
    return response.data;
};

export const getExportStatus = async () => {
    const response = await apiClient.get('analytics/export-status/');
    return response.data;
};