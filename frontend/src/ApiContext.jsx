import axios from 'axios';
import React, { createContext, useState } from 'react';

export const ApiContext = createContext();

export function ApiProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  const login = async (username, password) => {
    const resp = await api.post('/auth/token', new URLSearchParams({ username, password }));
    const t = resp.data.access_token;
    setToken(t);
    localStorage.setItem('token', t);
    api.defaults.headers.Authorization = `Bearer ${t}`;
    return t;
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
    delete api.defaults.headers.Authorization;
  };

  return (
    <ApiContext.Provider value={{ api, token, login, logout }}>
      {children}
    </ApiContext.Provider>
  );
}
