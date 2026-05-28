import React from 'react';

const MerchantSelector = ({ merchants, selectedMerchant, onSelect }) => {
    const merchantColors = {
        'Acme Corporation': '#3b82f6',      // Blue
        'Beta Industries': '#10b981',       // Green
    };
    
    return (
        <header style={styles.header}>
            <div style={styles.container}>
                <h1 style={styles.title}>
                    🏦 Merchant Analytics Dashboard
                </h1>
                
                <p style={styles.subtitle}>
                    Select a merchant to view their transaction data
                </p>
                
                <div style={styles.selectorGrid}>
                    {merchants.map((merchant) => (
                        <button
                            key={merchant.id}
                            onClick={() => onSelect(merchant)}
                            style={{
                                ...styles.merchantCard,
                                ...(selectedMerchant.id === merchant.id
                                    ? styles.merchantCardActive
                                    : {}),
                                borderLeftColor: merchantColors[merchant.name],
                            }}
                        >
                            <div style={styles.merchantCardContent}>
                                <h3 style={styles.merchantName}>
                                    {merchant.name}
                                </h3>
                                <p style={styles.merchantId}>
                                    ID: {merchant.id.slice(0, 8)}...
                                </p>
                                {selectedMerchant.id === merchant.id && (
                                    <span style={styles.activeIndicator}>
                                        ✓ Active
                                    </span>
                                )}
                            </div>
                        </button>
                    ))}
                </div>
            </div>
        </header>
    );
};

const styles = {
    header: {
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #e5e7eb',
        padding: '2rem 1rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    },
    container: {
        maxWidth: '1200px',
        margin: '0 auto',
    },
    title: {
        fontSize: '2rem',
        fontWeight: '700',
        color: '#1f2937',
        marginBottom: '0.5rem',
    },
    subtitle: {
        fontSize: '0.95rem',
        color: '#6b7280',
        marginBottom: '1.5rem',
    },
    selectorGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1rem',
    },
    merchantCard: {
        padding: '1.5rem',
        border: '2px solid #e5e7eb',
        borderLeft: '4px solid transparent',
        borderRadius: '0.5rem',
        backgroundColor: '#f9fafb',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        textAlign: 'left',
        fontSize: 'inherit',
        fontFamily: 'inherit',
    },
    merchantCardActive: {
        backgroundColor: '#eff6ff',
        borderColor: '#3b82f6',
        boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.1)',
    },
    merchantCardContent: {
        position: 'relative',
    },
    merchantName: {
        fontSize: '1.125rem',
        fontWeight: '600',
        color: '#1f2937',
        marginBottom: '0.5rem',
    },
    merchantId: {
        fontSize: '0.85rem',
        color: '#9ca3af',
        fontFamily: 'monospace',
    },
    activeIndicator: {
        display: 'inline-block',
        marginTop: '0.75rem',
        padding: '0.25rem 0.75rem',
        backgroundColor: '#10b981',
        color: '#ffffff',
        borderRadius: '1rem',
        fontSize: '0.85rem',
        fontWeight: '600',
    },
};

export default MerchantSelector;