import React, { useContext, useEffect, useState } from 'react';
import { ApiContext } from './ApiContext';

export function MovementsPage() {
  const { api } = useContext(ApiContext);
  const [movements, setMovements] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [productId, setProductId] = useState('');
  const [fromWh, setFromWh] = useState('');
  const [toWh, setToWh] = useState('');
  const [quantity, setQuantity] = useState('');
  const [note, setNote] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [movResp, prodResp, whResp] = await Promise.all([
        api.get('/movements/'),
        api.get('/products/'),
        api.get('/warehouses/'),
      ]);
      setMovements(movResp.data);
      setProducts(prodResp.data);
      setWarehouses(whResp.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/movements/', {
        product_id: parseInt(productId),
        from_warehouse_id: fromWh ? parseInt(fromWh) : null,
        to_warehouse_id: toWh ? parseInt(toWh) : null,
        quantity: parseInt(quantity),
        note,
      });
      setProductId('');
      setFromWh('');
      setToWh('');
      setQuantity('');
      setNote('');
      fetchData();
    } catch (err) {
      console.error('Error creating movement:', err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Inventory Movements</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: '20px' }}>
        <select
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          required
          style={{ padding: '8px', marginRight: '10px' }}
        >
          <option value="">Select Product</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          value={fromWh}
          onChange={(e) => setFromWh(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        >
          <option value="">From Warehouse (optional)</option>
          {warehouses.map((w) => (
            <option key={w.id} value={w.id}>
              {w.name}
            </option>
          ))}
        </select>
        <select
          value={toWh}
          onChange={(e) => setToWh(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        >
          <option value="">To Warehouse (optional)</option>
          {warehouses.map((w) => (
            <option key={w.id} value={w.id}>
              {w.name}
            </option>
          ))}
        </select>
        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <input
          type="text"
          placeholder="Note"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>
          Create Movement
        </button>
      </form>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0' }}>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>ID</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Product</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>From</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>To</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Qty</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Note</th>
          </tr>
        </thead>
        <tbody>
          {movements.map((m) => (
            <tr key={m.id}>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.id}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.product_id}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.from_warehouse_id || '—'}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.to_warehouse_id || '—'}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.quantity}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{m.note}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
