import React from 'react';

const TransactionTable = ({
    transactions,
    pagination,
    currentPage,
    onPageChange,
}) => {
    const getStatusColor = (status) => {
        const statusColors = {
            completed: '#10b981',
            pending: '#f59e0b',
            failed: '#ef4444',
            refunded: '#8b5cf6',
        };
        return statusColors[status] || '#6b7280';
    };
    
    const getStatusEmoji = (status) => {
        const statusEmojis = {
            completed: '✅',
            pending: '⏳',
            failed: '❌',
            refunded: '↩️',
        };
        return statusEmojis[status] || '•';
    };
    
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };
    
    if (!transactions || transactions.length === 0) {
        return (
            <div style={styles.emptyState}>
                <p>📭 No transactions found</p>
            </div>
        );
    }
    
    return (
        <div>
            {/* Table */}
            <div style={styles.tableWrapper}>
                <table style={styles.table}>
                    <thead>
                        <tr style={styles.headerRow}>
                            <th style={styles.th}>ID</th>
                            <th style={styles.th}>Amount</th>
                            <th style={styles.th}>Status</th>
                            <th style={styles.th}>Date</th>
                            <th style={styles.th}>Merchant</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map((tx) => (
                            <tr key={tx.id} style={styles.row}>
                                <td style={styles.td}>
                                    <code style={styles.txId}>
                                        {tx.id.slice(0, 8)}...
                                    </code>
                                </td>
                                <td style={styles.td}>
                                    <strong>
                                        ${parseFloat(tx.amount).toLocaleString()}
                                    </strong>
                                    <br />
                                    <span style={styles.currency}>
                                        {tx.currency}
                                    </span>
                                </td>
                                <td style={styles.td}>
                                    <span style={{
                                        ...styles.statusBadge,
                                        backgroundColor: getStatusColor(tx.status) + '20',
                                        color: getStatusColor(tx.status),
                                        borderColor: getStatusColor(tx.status),
                                    }}>
                                        {getStatusEmoji(tx.status)} {tx.status}
                                    </span>
                                </td>
                                <td style={styles.td}>
                                    <span style={styles.date}>
                                        {formatDate(tx.created_at)}
                                    </span>
                                </td>
                                <td style={styles.td}>
                                    {tx.merchant_name}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            
            {/* Pagination */}
            {pagination.count > 20 && (
                <div style={styles.pagination}>
                    <button
                        onClick={() => onPageChange(currentPage - 1)}
                        disabled={!pagination.previous}
                        style={{
                            ...styles.paginationButton,
                            ...(pagination.previous ? {} : styles.paginationButtonDisabled),
                        }}
                    >
                        ← Previous
                    </button>
                    
                    <span style={styles.pageInfo}>
                        Page {currentPage} of{' '}
                        {Math.ceil(pagination.count / 20)}
                    </span>
                    
                    <button
                        onClick={() => onPageChange(currentPage + 1)}
                        disabled={!pagination.next}
                        style={{
                            ...styles.paginationButton,
                            ...(pagination.next ? {} : styles.paginationButtonDisabled),
                        }}
                    >
                        Next →
                    </button>
                </div>
            )}
        </div>
    );
};

const styles = {
    emptyState: {
        textAlign: 'center',
        padding: '2rem',
        color: '#9ca3af',
        fontSize: '1.125rem',
    },
    tableWrapper: {
        overflowX: 'auto',
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '0.95rem',
    },
    headerRow: {
        backgroundColor: '#f9fafb',
        borderBottom: '2px solid #e5e7eb',
    },
    th: {
        padding: '1rem',
        textAlign: 'left',
        fontWeight: '600',
        color: '#1f2937',
    },
    row: {
        borderBottom: '1px solid #e5e7eb',
        transition: 'background-color 0.2s',
    },
    td: {
        padding: '1rem',
        color: '#374151',
    },
    txId: {
        backgroundColor: '#f3f4f6',
        padding: '0.25rem 0.5rem',
        borderRadius: '0.25rem',
        fontFamily: 'monospace',
        fontSize: '0.85rem',
    },
    currency: {
        fontSize: '0.85rem',
        color: '#9ca3af',
    },
    statusBadge: {
        display: 'inline-block',
        padding: '0.25rem 0.75rem',
        borderRadius: '0.375rem',
        fontSize: '0.85rem',
        fontWeight: '600',
        border: '1px solid',
    },
    date: {
        color: '#6b7280',
        fontSize: '0.9rem',
    },
    pagination: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '1rem',
        marginTop: '2rem',
        paddingTop: '1.5rem',
        borderTop: '1px solid #e5e7eb',
    },
    paginationButton: {
        padding: '0.5rem 1rem',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        border: 'none',
        borderRadius: '0.375rem',
        cursor: 'pointer',
        fontSize: '0.9rem',
        fontWeight: '600',
        transition: 'background-color 0.2s',
    },
    paginationButtonDisabled: {
        backgroundColor: '#d1d5db',
        cursor: 'not-allowed',
    },
    pageInfo: {
        color: '#6b7280',
        fontSize: '0.95rem',
    },
};

export default TransactionTable;