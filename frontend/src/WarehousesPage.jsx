import React, { useContext, useEffect, useState } from 'react';
import { ApiContext } from './ApiContext';

export function WarehousesPage() {
  const { api } = useContext(ApiContext);
  const [warehouses, setWarehouses] = useState([]);
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');

  useEffect(() => {
    fetchWarehouses();
  }, []);

  const fetchWarehouses = async () => {
    try {
      const resp = await api.get('/warehouses/');
      setWarehouses(resp.data);
    } catch (err) {
      console.error('Error fetching warehouses:', err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/warehouses/', { name, location });
      setName('');
      setLocation('');
      fetchWarehouses();
    } catch (err) {
      console.error('Error creating warehouse:', err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Warehouses</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Warehouse name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>
          Add Warehouse
        </button>
      </form>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0' }}>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>ID</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Location</th>
          </tr>
        </thead>
        <tbody>
          {warehouses.map((w) => (
            <tr key={w.id}>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{w.id}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{w.name}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{w.location}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
