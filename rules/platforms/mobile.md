# Mobile Application Engineering Guidelines & Best Practices

Strict architectural and usability standards for Mobile applications (React Native, Expo, Flutter, Native iOS/Android).

---

## 1. UX, Touch Targets & Viewport Adaptation

1. **Touch Targets & Safe Areas**:
   - Ensure all interactive touch targets meet minimum accessible dimensions (at least `44x44` logical pixels / points).
   - Always wrap root views in Safe Area containers to prevent UI clipping under hardware notches, status bars, and home indicators.

2. **Keyboard Handling & Viewport Resizing**:
   - Use adaptive keyboard avoiding views to prevent virtual keyboards from obscuring active input fields or submit buttons.

---

## 2. Offline-First & Data Synchronization

1. **Local Persistent Storage**:
   - Cache domain entities locally using embedded storage (SQLite, WatermelonDB, or MMKV for high-performance key-value pairs).
   - Queue outgoing mutations in an offline outbox and replay them with exponential backoff upon network reconnection.

2. **Conflict Resolution**:
   - Implement deterministic conflict resolution strategies (e.g. server-wins or CRDT-based merging) for offline edits.

---

## 3. Device Permissions & State Lifecycle

1. **Just-in-Time Permissions**:
   - Request hardware permissions (Camera, Location, Push Notifications, Photos) contextual to user actions with clear explanations, never on first app launch.

2. **App State Transitions**:
   - Handle transitions between `active`, `background`, and `inactive` states. Pause heavy polling, animations, or location listeners when moving to the background.

---

## 4. Performance, Memory & Battery Optimization

1. **Image Optimization**:
   - Downsample and resize remote images according to screen pixel density before rendering; avoid loading raw multi-megabyte bitmaps into memory.

2. **Battery & Background Limits**:
   - Adhere to platform background execution limits (WorkManager on Android, BGTaskScheduler on iOS). Avoid keeping continuous wake-locks.

