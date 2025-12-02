import React, { useContext, useEffect, useState } from 'react';
import { ApiContext } from './ApiContext';

export function ProductsPage() {
  const { api } = useContext(ApiContext);
  const [products, setProducts] = useState([]);
  const [name, setName] = useState('');
  const [sku, setSku] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const resp = await api.get('/products/');
      setProducts(resp.data);
    } catch (err) {
      console.error('Error fetching products:', err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/products/', { name, sku, price: parseFloat(price) });
      setName('');
      setSku('');
      setPrice('');
      fetchProducts();
    } catch (err) {
      console.error('Error creating product:', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/products/${id}`);
      fetchProducts();
    } catch (err) {
      console.error('Error deleting product:', err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Products</h2>
      <form onSubmit={handleCreate} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Product name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <input
          type="text"
          placeholder="SKU"
          value={sku}
          onChange={(e) => setSku(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          step="0.01"
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>
          Add Product
        </button>
      </form>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0' }}>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>ID</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>SKU</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Price</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((prod) => (
            <tr key={prod.id}>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{prod.id}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{prod.name}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>{prod.sku}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>${prod.price}</td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                <button onClick={() => handleDelete(prod.id)} style={{ color: 'red' }}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
