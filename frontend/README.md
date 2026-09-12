# ma-famille frontend (Vue 3 + Vite + Pinia + Tailwind CSS v4)

Foundation iteration: router + Pinia + axios client + Tailwind + health views.
No domain CRUD yet (Venue/Court/Slot/Booking/Payment come next).

## Dev

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build to dist/
```

Env: copy `.env.example` to `.env`, set `VITE_API_URL` (default `http://localhost:8000`).

## Layout

```text
src/
  router/index.js     # /, /health
  services/api.js     # single axios instance + fetchHealth/fetchRoot
  stores/app.js       # backend connectivity state
  views/              # HomeView, HealthView
  components/         # AppNav, HealthStatus
  App.vue main.js
```

Rules:

- Styling via Tailwind utilities (`src/style.css` only contains `@import 'tailwindcss'`).
- HTTP only via `services/api.js`.
- Server state in Pinia stores, one file per domain (`venues.js`, `bookings.js`, … next).
- Views are thin; reusable UI goes to `components/`.
