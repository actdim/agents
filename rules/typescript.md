# TypeScript Coding Standards & Best Practices

Strict TypeScript conventions for production-grade, maintainable codebases.

---

## 1. Strict Typing & Zero `any`
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

## 2. Types vs Interfaces & Data Modeling
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

## 3. Immutability & Modern Conventions
- **Readonly Collections**: Prefer `ReadonlyArray<T>` or `readonly T[]` and `as const` assertions for immutable configuration and lookup tables.
- **Optional Chaining & Nullish Coalescing**: Prefer `?.` and `??` over verbose logical checks (`&&` or `||`).
- **Exact Optional Properties**: Explicitly distinguish between `undefined` and missing properties.

---

## 4. Naming & File Organization
- **PascalCase**: Classes, Interfaces, Types, Enums, React Components.
- **camelCase**: Variables, functions, methods, properties.
- **UPPER_SNAKE_CASE**: Global constants.
- **kebab-case**: Source filenames (e.g. `user-service.ts`, `auth-guard.ts`).

