import React, { useState, useEffect } from 'react';
import { requestExport, getExportStatus } from '../api/client';

const ExportButton = ({ onExportComplete }) => {
    const [isExporting, setIsExporting] = useState(false);
    const [exportStatus, setExportStatus] = useState(null);
    const [statusMessage, setStatusMessage] = useState('');

    const handleRequestExport = async () => {
        try {
            setIsExporting(true);
            setStatusMessage('📤 Requesting export...');
            
            // Send export request (returns 202)
            const result = await requestExport('csv');
            
            setStatusMessage('⏳ Processing export in background...');
            
            // Start polling for status
            pollExportStatus();
        } catch (error) {
            setStatusMessage('❌ Export failed: ' + error.message);
            setIsExporting(false);
        }
    };

    const pollExportStatus = async () => {
        const maxAttempts = 30;  
        let attempts = 0;
        
        const poll = async () => {
            try {
                const status = await getExportStatus();
                
                if (status.status === 'processing') {
                    setStatusMessage(
                        `⏳ Processing... (${attempts + 1}s)`
                    );
                    
                    // Poll again in 1 second
                    if (attempts < maxAttempts) {
                        attempts++;
                        setTimeout(poll, 1000);
                    } else {
                        setStatusMessage('⚠️ Export timed out');
                        setIsExporting(false);
                    }
                } else if (status.status === 'complete') {
                    setStatusMessage(
                        `✅ Export complete! ${status.rows} rows, ` +
                        `${status.file_size_kb?.toFixed(1)}KB`
                    );
                    setExportStatus(status);
                    setIsExporting(false);
                } else if (status.status === 'error') {
                    setStatusMessage(`❌ Export error: ${status.error}`);
                    setIsExporting(false);
                } else {
                    setStatusMessage(`⏳ Status: ${status.status}`);
                    attempts++;
                    if (attempts < maxAttempts) {
                        setTimeout(poll, 1000);
                    }
                }
            } catch (error) {
                console.error('Status poll error:', error);
                setStatusMessage('⚠️ Failed to check status');
                setIsExporting(false);
            }
        };
        
        poll();
    };
    
    const handleDownloadMock = () => {
        alert('📥 In production, this would download the CSV file');
    };
    
    return (
        <div style={styles.container}>
            <button
                onClick={handleRequestExport}
                disabled={isExporting}
                style={{
                    ...styles.exportButton,
                    ...(isExporting ? styles.exportButtonDisabled : {}),
                }}
            >
                {isExporting ? '⏳ Exporting...' : '📥 Export Report (CSV)'}
            </button>
            
            {statusMessage && (
                <div style={{
                    ...styles.statusMessage,
                    ...getStatusStyle(statusMessage),
                }}>
                    {statusMessage}
                </div>
            )}
            
            {exportStatus && exportStatus.status === 'complete' && (
                <div style={styles.downloadSection}>
                    <button
                        onClick={handleDownloadMock}
                        style={styles.downloadButton}
                    >
                        📁 Download Report
                    </button>
                    <p style={styles.fileInfo}>
                        Generated: {new Date(exportStatus.completed_at).toLocaleString()}
                    </p>
                </div>
            )}
        </div>
    );
};

const getStatusStyle = (message) => {
    if (message.includes('❌')) {
        return {
            backgroundColor: '#fef2f2',
            borderColor: '#fee2e2',
            color: '#991b1b',
        };
    } else if (message.includes('✅')) {
        return {
            backgroundColor: '#f0fdf4',
            borderColor: '#dcfce7',
            color: '#166534',
        };
    } else {
        return {
            backgroundColor: '#fffbeb',
            borderColor: '#fef3c7',
            color: '#92400e',
        };
    }
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
    },
    exportButton: {
        padding: '0.75rem 1.5rem',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        border: 'none',
        borderRadius: '0.5rem',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
        maxWidth: '200px',
    },
    exportButtonDisabled: {
        backgroundColor: '#9ca3af',
        cursor: 'not-allowed',
    },
    statusMessage: {
        padding: '1rem',
        borderRadius: '0.5rem',
        border: '1px solid',
        fontSize: '0.95rem',
        fontWeight: '500',
    },
    downloadSection: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
    },
    downloadButton: {
        padding: '0.75rem 1.5rem',
        backgroundColor: '#10b981',
        color: '#ffffff',
        border: 'none',
        borderRadius: '0.5rem',
        fontSize: '0.95rem',
        fontWeight: '600',
        cursor: 'pointer',
        maxWidth: '200px',
        transition: 'background-color 0.2s',
    },
    fileInfo: {
        fontSize: '0.85rem',
        color: '#6b7280',
        margin: 0,
    },
};

export default ExportButton;