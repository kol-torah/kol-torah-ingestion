# Kol Torah Admin Frontend

React + TypeScript + Material UI frontend for the Kol Torah admin interface.

## Setup

1. **Install dependencies:**
   ```bash
   pnpm install
   ```

2. **Make sure the backend is running:**
   The frontend expects the API to be running at `http://localhost:8000`

## Running the Application

### Development Mode:
```bash
pnpm dev
```

The application will be available at http://localhost:5173

### Build for Production:
```bash
pnpm build
```

### Preview Production Build:
```bash
pnpm preview
```

## Features

- **Rabbi Management:**
  - View all rabbis
  - Create new rabbis
  - Edit existing rabbis
  - Delete rabbis (cascades to all their series)
  - Select a rabbi to view their series

- **Series Management:**
  - View all series for a selected rabbi
  - Create new series for a rabbi
  - Edit existing series
  - Delete series

## Project Structure

```
admin/frontend/
├── src/
│   ├── components/
│   │   ├── RabbiDialog.tsx    # Dialog for creating/editing rabbis
│   │   └── SeriesDialog.tsx   # Dialog for creating/editing series
│   ├── api.ts                 # API client functions
│   ├── types.ts               # TypeScript type definitions
│   ├── App.tsx                # Main application component
│   ├── main.tsx               # Application entry point
│   ├── App.css                # Application styles
│   └── index.css              # Global styles
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Material UI (MUI)** - Component library
- **Axios** - HTTP client
- **Vite** - Build tool and dev server

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`:

- `GET /rabbis/` - List all rabbis
- `POST /rabbis/` - Create a rabbi
- `PUT /rabbis/{id}` - Update a rabbi
- `DELETE /rabbis/{id}` - Delete a rabbi
- `GET /series/by-rabbi/{rabbi_id}` - Get series for a rabbi
- `POST /series/` - Create a series
- `PUT /series/{id}` - Update a series
- `DELETE /series/{id}` - Delete a series
