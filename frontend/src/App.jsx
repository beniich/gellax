import React, { useContext, useState } from 'react';
import { ApiContext } from './ApiContext';
import { LoginPage } from './LoginPage';
import { ProductsPage } from './ProductsPage';
import { WarehousesPage } from './WarehousesPage';
import { MovementsPage } from './MovementsPage';

function App() {
  const { token, logout } = useContext(ApiContext);
  const [currentPage, setCurrentPage] = useState('products');

  if (!token) {
    return <LoginPage onLoginSuccess={() => setCurrentPage('products')} />;
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      <nav style={{ backgroundColor: '#333', color: '#fff', padding: '10px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between' }}>
          <h1 style={{ margin: 0 }}>Gellax</h1>
          <div>
            <button
              onClick={() => setCurrentPage('products')}
              style={{
                marginRight: '10px',
                padding: '8px 16px',
                backgroundColor: currentPage === 'products' ? '#0066cc' : 'transparent',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Products
            </button>
            <button
              onClick={() => setCurrentPage('warehouses')}
              style={{
                marginRight: '10px',
                padding: '8px 16px',
                backgroundColor: currentPage === 'warehouses' ? '#0066cc' : 'transparent',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Warehouses
            </button>
            <button
              onClick={() => setCurrentPage('movements')}
              style={{
                marginRight: '10px',
                padding: '8px 16px',
                backgroundColor: currentPage === 'movements' ? '#0066cc' : 'transparent',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Movements
            </button>
            <button
              onClick={logout}
              style={{
                padding: '8px 16px',
                backgroundColor: '#cc0000',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {currentPage === 'products' && <ProductsPage />}
        {currentPage === 'warehouses' && <WarehousesPage />}
        {currentPage === 'movements' && <MovementsPage />}
      </main>
    </div>
  );
}

export default App;
