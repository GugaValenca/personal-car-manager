# Personal Car Manager Frontend

React + TypeScript, but scoped to the login/signup screens only - see the
"About the architecture, honestly" section in the repo's main README for why.
Everything past login is server-rendered Django, not this.

## Stack
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui (only `toast`, `sonner` and `tooltip` are actually in use)

## Development
```bash
npm install
npm run dev
```
This runs Vite's own dev server on `http://127.0.0.1:8080`. It's just for
iterating on the login/signup screens in isolation - `/auth/login/` won't
resolve here since that's a Django route, so submitting the form will fail
unless Django is also running separately on `127.0.0.1:8000` and you're
hitting these pages through it instead.

## Build
```bash
npm run build
```
Copy the output from `dist/assets/` plus `dist/.vite/manifest.json` into the
main project's `static/app/` - that's what Django actually serves in
production. See the root README for the full loop.
