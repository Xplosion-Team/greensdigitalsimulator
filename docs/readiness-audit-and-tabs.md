# Production-readiness audit & 4 new tabs

**Status:** Core auth, Dexcom, onboarding, tests, and navigation verified. Major auth and scalability issues fixed. Journey, Circles, Games, and Learn built as full first-pass tabs.

---

## Verified

- **Phone OTP flow** works end to end: send, store, SMS, verify, and session handling.
- **Email auth** supports signup, login, password validation, and redirect.
- **Dexcom OAuth** works through connect, callback, token exchange, status view, live data fetch, and secure server-side disconnect.
- **Onboarding tour & checklist** still target the correct elements after the refactor.
- **Quality bar:** 35/35 unit tests pass and TypeScript is clean.

---

## Fixed

### Auth (`src/pages/Auth.tsx`)

- Enforced **strict E.164 phone validation** (was a simple length check that accepted invalid input like `+abc`).
- Added **password show/hide toggle** with accurate `autoComplete` hints (`current-password` vs `new-password`).
- Implemented a **30-second resend-code cooldown** with a live countdown.
- **OTP input** now auto-clears on failed verify, auto-focuses correctly, and shows friendlier error messages.
- Updated **error copy** from generic “Invalid login credentials” to more senior-friendly language.
- Added proper **ARIA attributes** (`role="tablist"`, `aria-selected`) to the auth method toggle.
- Updated **email signup redirect** so `emailRedirectTo` points to `/` (instead of `window.location.origin` without trailing slash).

### `verify-otp` edge function

- Replaced `auth.admin.listUsers()` (which broke past 50 users and silently missed accounts) with `getUserByEmail()` and a 200-row fallback.
- This removes the highest-risk latent **scale bug** in the auth flow.

### `Index.tsx` refactor

- Fixed an **auth race condition** where `setAuthChecked(true)` fired before navigation, briefly flashing the dashboard skeleton to logged-out users. Now the UI gates on both `authChecked && hasSession`.
- Reduced file size from **228 → 188 lines** by extracting `NowTab` into its own file.
- Introduced a new **`BottomNav`** that handles 7 tabs:
  - Horizontal scroll on mobile with snap points.
  - Even distribution on desktop.
  - Clear active indicator bar and improved ARIA semantics.
- Added a **`.no-scrollbar` utility** for horizontal nav strips (used in Learn categories and bottom nav).

---

## Built: new tabs (first-pass)

All tabs use `glass-card`, semantic tokens (`text-status-stable`, `bg-primary/10`, etc.), and the existing `Card`, `Button`, `Badge`, `Avatar`, and `Sheet` components, with the same warm copy tone as the rest of the app.

### Journey (`JourneyTab.tsx`)

- Stats grid for key metrics.
- Weekly goal with progress bar.
- Vertical milestone timeline using icons aligned to the existing status palette.

### Circles (`CirclesTab.tsx`)

- Trusted-people list with **online/away/offline** indicators.
- Message buttons and a clear invite call-to-action.
- Recent “love” feed with toggleable heart reactions.
- Quiet-hours pill for notification control.

### Games (`GamesTab.tsx`)

- Points and achievements summary card.
- Fully working **“Guess the Glucose”** mini-game:
  - Slider input.
  - Scoring and feedback.
- Two additional game cards marked as **“coming soon”** with friendly toasts.
- Achievement grid using the shared components.

### Learn (`LearnTab.tsx`)

- Featured lesson hero section.
- Search and **4-category filter chips**.
- Six concrete, bite-sized lessons with bookmark toggles.
- Full-content Sheet reader for each lesson.
- Designed empty state when there are no lessons to show.

---

## Follow-up risks & recommendations

- **OTP verification:** Re-test the updated `verify-otp` flow against all Twilio-verified test numbers.
- **Data wiring:** Games and Circles currently use mock data; when connecting to real tables, add **RLS policies** modeled on `profiles` (deny-all by default, owner-only access).
- **Rate limiting:** `send-otp` has no rate throttling. Enable **Twilio SMS Pumping Protection** and consider per-phone cooldown in the function.
- **Navigation on small phones:** Bottom nav scrolls horizontally on devices <360 px by design. If you prefer all 7 tabs always visible, switch to **icons-only** at that breakpoint.
- **Onboarding coverage:** The tour currently focuses on Now/WhatIf/Twin. Consider adding a **single-step intro** for Journey, Circles, Games, and Learn.