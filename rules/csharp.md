# C# / .NET Coding Standards & Best Practices

Modern .NET 8+ and C# 12 engineering conventions based on Microsoft Framework Design Guidelines and high-performance patterns.

---

## 1. Type Safety & Nullability
- **Nullable Reference Types**: Always enable `<Nullable>enable</Nullable>` in `.csproj`.
- **Zero Null Suppressions**: Avoid `!` (null-forgiving operator) unless mathematically guaranteed and documented. Use null-coalescing (`??`, `??=`) and null-conditional (`?.`) operators.
- **Pattern Matching**: Prefer pattern matching (`is`, `switch` expressions) over explicit casting (`as`, `(Type)`).

```csharp
// Recommended: Pattern matching with null check
if (user is { IsActive: true, Email: { Length: > 0 } email })
{
    await SendNotificationAsync(email, cancellationToken);
}
```

---

## 2. Immutability & Data Modeling
- **Records**: Use `record` or `record struct` for DTOs, events, and value objects.
- **Readonly Structs**: Use `readonly struct` for small, high-throughput value types to eliminate defensive copying.
- **Primary Constructors**: Use C# 12 primary constructors on classes and records for clean dependency injection.

```csharp
// Recommended: Primary constructor dependency injection
public sealed class OrderService(
    IOrderRepository repository,
    ILogger<OrderService> logger) : IOrderService
{
    public async Task<OrderResult> ProcessAsync(OrderId id, CancellationToken ct = default)
    {
        // ...
    }
}
```

---

## 3. Asynchronous Programming Guidelines
- **Always Pass `CancellationToken`**: Every async method accepting external I/O must accept and propagate a `CancellationToken`.
- **No `async void`**: Use `async void` strictly for event handlers; all other async methods must return `Task` or `ValueTask`.
- **ValueTask for Hot Paths**: Return `ValueTask<T>` for high-frequency methods that frequently complete synchronously (e.g. cache lookups).
- **Avoid `.Result` and `.Wait()`**: Never block on asynchronous code (prevents thread-pool starvation and deadlocks).

---

## 4. Naming & Formatting Conventions
- **PascalCase**: Classes, Records, Structs, Enums, Interfaces, Methods, Properties, Public fields.
- **camelCase**: Local variables, method arguments, private fields with `_` prefix (e.g. `_orderRepository`).
- **Interfaces**: Always prefix with `I` (e.g. `IUserService`).
- **Async Suffix**: Always append `Async` to asynchronous methods (e.g. `FetchUserDataAsync`).
- **File-scoped Namespaces**: Use file-scoped namespaces (`namespace MyProject.Services;`) to reduce indentation.

