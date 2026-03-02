# Personal Car Manager Frontend (Lovable)

React + TypeScript frontend exported from Lovable and integrated into the `personal-car-manager` monorepo.

## Stack
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui

## Development
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
```

## API Integration
The frontend consumes the backend endpoint:
- `GET /api/dashboard/`

For local development, run Django backend on:
- `http://127.0.0.1:8000`

Then run this frontend on:
- `http://127.0.0.1:5173`
