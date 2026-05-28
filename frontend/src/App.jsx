/**
 * MAIN APPLICATION COMPONENT
 * 
 * Architecture:
 * - Manages global merchant selection state
 * - Routes to Dashboard with merchant context
 * - Handles real-time data refresh
 */

import React, { useState, useEffect } from 'react';
import { setMerchantId } from './api/client';
import Dashboard from './components/Dashboard';
import MerchantSelector from './components/MerchantSelector';

const App = () => {
    const MERCHANTS = [
        {
            id: '5365b384-da2a-40bf-b47c-f10d336db4df',  // Replace with actual seeded UUID
            name: 'Acme Corporation',
        },
        {
            id: '0179bb69-75d7-49b8-bca8-08cfcfcf4b16',  // Replace with actual seeded UUID
            name: 'Beta Industries',
        },
    ];
    
    const [selectedMerchant, setSelectedMerchant] = useState(MERCHANTS[0]);
    const [refreshKey, setRefreshKey] = useState(0);
    
    /**
     * Update merchant ID when selection changes.
     * 
     * Side effect: All subsequent API calls will use new merchant context.
     */
    useEffect(() => {
        setMerchantId(selectedMerchant.id);
    }, [selectedMerchant]);
    
    const handleMerchantChange = (merchant) => {
        setSelectedMerchant(merchant);
        // Force dashboard refresh when merchant changes
        setRefreshKey(prev => prev + 1);
    };
    
    const handleRefresh = () => {
        setRefreshKey(prev => prev + 1);
    };
    
    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f5f7fa' }}>
            {/* Merchant Selection Header */}
            <MerchantSelector
                merchants={MERCHANTS}
                selectedMerchant={selectedMerchant}
                onSelect={handleMerchantChange}
            />
            
            {/* Main Dashboard */}
            <Dashboard
                merchant={selectedMerchant}
                refreshKey={refreshKey}
                onRefresh={handleRefresh}
            />
        </div>
    );
};

export default App;