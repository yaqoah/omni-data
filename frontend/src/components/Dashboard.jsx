import React, { useState, useEffect, useCallback } from 'react';
import { fetchAnalyticsSummary, fetchTransactions } from '../api/client';
import TransactionTable from './TransactionTable';
import ExportButton from './ExportButton';

const Dashboard = ({ merchant, refreshKey, onRefresh }) => {
    const [analytics, setAnalytics] = useState(null);
    const [transactions, setTransactions] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);

    const loadDashboardData = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            // Parallel requests for analytics and transactions
            const [analyticsData, transactionsData] = await Promise.all([
                fetchAnalyticsSummary(),
                fetchTransactions(currentPage),
            ]);
            
            setAnalytics(analyticsData);
            setTransactions(transactionsData);
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                err.message ||
                'Failed to load dashboard data'
            );
            console.error('Dashboard load error:', err);
        } finally {
            setLoading(false);
        }
    }, [currentPage]);
    
    useEffect(() => {
        loadDashboardData();
    }, [refreshKey, currentPage, loadDashboardData]);
    
    if (loading) {
        return (
            <div style={styles.container}>
                <div style={styles.loadingMessage}>
                    ⏳ Loading dashboard data...
                </div>
            </div>
        );
    }
    
    if (error) {
        return (
            <div style={styles.container}>
                <div style={styles.errorMessage}>
                    <strong>⚠️ Error:</strong> {error}
                </div>
                <button onClick={onRefresh} style={styles.retryButton}>
                    🔄 Retry
                </button>
            </div>
        );
    }
    
    return (
        <div style={styles.container}>
            {/* Header with merchant context */}
            <div style={styles.dashboardHeader}>
                <div>
                    <h2 style={styles.dashboardTitle}>
                        {merchant.name} - Transaction Analytics
                    </h2>
                    <p style={styles.dashboardSubtitle}>
                        Real-time view of all transactions and activity
                    </p>
                </div>
                <button onClick={onRefresh} style={styles.refreshButton}>
                    🔄 Refresh Data
                </button>
            </div>
            
            {/* Analytics Summary Grid */}
            {analytics && (
                <div style={styles.metricsGrid}>
                    <MetricCard
                        label="Total Transactions"
                        value={analytics.total}
                        icon="📊"
                    />
                    <MetricCard
                        label="Completed"
                        value={analytics.completed}
                        icon="✅"
                        color="#10b981"
                    />
                    <MetricCard
                        label="Pending"
                        value={analytics.pending}
                        icon="⏳"
                        color="#f59e0b"
                    />
                    <MetricCard
                        label="Failed"
                        value={analytics.failed}
                        icon="❌"
                        color="#ef4444"
                    />
                    <MetricCard
                        label="Total Volume"
                        value={parseFloat(analytics.total_volume || 0).toLocaleString()}
                        icon="💰"
                        color="#3b82f6"
                    />
                    <MetricCard
                        label="Average Transaction"
                        value={parseFloat(analytics.average_transaction || 0).toLocaleString()}
                        icon="📈"
                        color="#8b5cf6"
                    />
                </div>
            )}
            
            {/* Export Section */}
            <div style={styles.exportSection}>
                <h3 style={styles.sectionTitle}>📋 Export Report</h3>
                <ExportButton onExportComplete={onRefresh} />
            </div>
            
            {/* Transactions Table */}
            <div style={styles.transactionsSection}>
                <h3 style={styles.sectionTitle}>📑 Recent Transactions</h3>
                {transactions && (
                    <TransactionTable
                        transactions={transactions.results}
                        pagination={transactions}
                        currentPage={currentPage}
                        onPageChange={setCurrentPage}
                    />
                )}
            </div>
        </div>
    );
};

/**
 * METRIC CARD COMPONENT
 * 
 * Displays a single metric in a styled card.
 */
const MetricCard = ({ label, value, icon = '📊', color = '#6b7280' }) => (
    <div style={{
        ...styles.metricCard,
        borderLeftColor: color,
    }}>
        <div style={styles.metricIcon}>{icon}</div>
        <div>
            <p style={styles.metricLabel}>{label}</p>
            <p style={{
                ...styles.metricValue,
                color: color,
            }}>
                {value}
            </p>
        </div>
    </div>
);

const styles = {
    container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '2rem 1rem',
    },
    dashboardHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '2rem',
        flexWrap: 'wrap',
        gap: '1rem',
    },
    dashboardTitle: {
        fontSize: '1.875rem',
        fontWeight: '700',
        color: '#1f2937',
    },
    dashboardSubtitle: {
        fontSize: '0.95rem',
        color: '#6b7280',
        marginTop: '0.25rem',
    },
    refreshButton: {
        padding: '0.75rem 1.5rem',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        border: 'none',
        borderRadius: '0.5rem',
        fontSize: '0.95rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    metricsGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem',
    },
    metricCard: {
        backgroundColor: '#ffffff',
        border: '1px solid #e5e7eb',
        borderLeft: '4px solid #6b7280',
        borderRadius: '0.5rem',
        padding: '1.5rem',
        display: 'flex',
        alignItems: 'flex-start',
        gap: '1rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    },
    metricIcon: {
        fontSize: '1.75rem',
    },
    metricLabel: {
        fontSize: '0.875rem',
        color: '#6b7280',
        fontWeight: '500',
        margin: 0,
    },
    metricValue: {
        fontSize: '1.75rem',
        fontWeight: '700',
        margin: '0.25rem 0 0 0',
    },
    exportSection: {
        backgroundColor: '#ffffff',
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
        padding: '1.5rem',
        marginBottom: '2rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    },
    transactionsSection: {
        backgroundColor: '#ffffff',
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
        padding: '1.5rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    },
    sectionTitle: {
        fontSize: '1.25rem',
        fontWeight: '600',
        color: '#1f2937',
        marginBottom: '1rem',
    },
    loadingMessage: {
        textAlign: 'center',
        padding: '2rem',
        fontSize: '1.125rem',
        color: '#6b7280',
    },
    errorMessage: {
        backgroundColor: '#fef2f2',
        border: '1px solid #fee2e2',
        color: '#991b1b',
        padding: '1rem',
        borderRadius: '0.5rem',
        marginBottom: '1rem',
    },
    retryButton: {
        padding: '0.75rem 1.5rem',
        backgroundColor: '#ef4444',
        color: '#ffffff',
        border: 'none',
        borderRadius: '0.5rem',
        fontSize: '0.95rem',
        cursor: 'pointer',
    },
};

export default Dashboard;