# Gellax Frontend

React + Vite frontend for the Gellax merchandise management platform.

## Setup

```bash
cd frontend
npm install
npm run dev
```

The dev server will start on `http://localhost:3000` and proxy API calls to `http://localhost:8000`.

## Features

- **Login**: OAuth2 password flow via JWT
- **Products**: CRUD for managing products
- **Warehouses**: View and create warehouses
- **Movements**: Record inventory movements between warehouses

## Building

```bash
npm run build
```

Output is in `dist/`.
