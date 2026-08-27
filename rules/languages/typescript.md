# TypeScript Coding Standards & Best Practices

Strict TypeScript conventions for production-grade, maintainable codebases and monorepos.

---

## 1. Monorepos & Workspace Dependency Management

- **PNPM Workspaces Standard**:
  - In multi-package or multi-platform repositories, use PNPM workspaces (`pnpm-workspace.yaml`) to manage dependencies across packages.
  - Link internal repository packages using the `workspace:*` protocol (e.g. `"@myorg/core": "workspace:*"`). `pnpm publish` automatically resolves and replaces `workspace:*` with exact semver versions when publishing to a registry.
  - Use PNPM Catalogs (`pnpm:catalog:`) in the root `pnpm-workspace.yaml` to enforce uniform external dependency versions (React, TypeScript, Vitest, MSW) across all workspace members without version drift.

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/*"

catalog:
  typescript: ^5.5.0
  vitest: ^2.0.0
  msw: ^2.4.0
```

---

## 2. Strict Typing & Zero `any`

- **Compiler Configuration**: Enforce `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true`, `"noUncheckedIndexedAccess": true`.
- **Ban `any`**: Never use `any`. Use `unknown` when the type is truly dynamic, and narrow it using type guards (`typeof`, `instanceof`, custom type predicates).
- **Explicit Return Types**: All exported functions and API boundaries must declare explicit return types.

```typescript
// Recommended: Type guard with unknown
function isApiResponse(data: unknown): data is { success: boolean; data: string } {
  return (
    typeof data === "object" &&
    data !== null &&
    "success" in data &&
    typeof (data as Record<string, unknown>).success === "boolean"
  );
}
```

---

## 3. Types vs Interfaces & Data Modeling

- **Interfaces for Object Shapes & Extension**: Use `interface` for object contracts, classes, and public APIs that may be augmented.
- **Type Aliases for Unions & Utilities**: Use `type` for unions, intersections, primitives, tuples, and mapped types.
- **Discriminated Unions**: Model domain states using discriminated unions with a common literal discriminator field (e.g. `type` or `status`).

```typescript
// Recommended: Discriminated union
type AsyncResult<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };
```

---

## 4. Immutability & Modern Conventions

- **Readonly Collections**: Prefer `ReadonlyArray<T>` or `readonly T[]` and `as const` assertions for immutable configuration and lookup tables.
- **Optional Chaining & Nullish Coalescing**: Prefer `?.` and `??` over verbose logical checks (`&&` or `||`).
- **Exact Optional Properties**: Explicitly distinguish between `undefined` and missing properties.

---

## 5. Naming & File Organization

- **PascalCase**: Classes, Interfaces, Types, Enums, React Components.
- **camelCase**: Variables, functions, methods, properties.
- **UPPER_SNAKE_CASE**: Global constants.
- **kebab-case**: Source filenames (e.g. `user-service.ts`, `auth-guard.ts`).

