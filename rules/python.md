# Python Coding Standards & Best Practices

Modern Python 3.11+ engineering conventions based on PEP 8, Google Python Style Guide, and strict static type analysis.

---

## 1. Static Type Annotations
- **Strict Typing**: Type annotate all function arguments and return types. Avoid `Any` where possible.
- **Modern Syntax**: Use Python 3.10+ union syntax (`X | Y` instead of `Union[X, Y]`, `list[str]` instead of `List[str]`).
- **Type Checking**: Ensure code passes `mypy --strict` or `pyright` without errors.

```python
# Recommended: Modern type hints and dataclass
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True, slots=True)
class Coordinate:
    x: float
    y: float

    @classmethod
    def from_tuple(cls, val: tuple[float, float]) -> Self:
        return cls(x=val[0], y=val[1])
```

---

## 2. Data Structures & Immutability
- **Dataclasses & Pydantic**: Use `@dataclass(frozen=True, slots=True)` for internal value objects and Pydantic `BaseModel` for external API validation.
- **Generators & Iterators**: Use generator expressions (`(x for x in data)`) instead of eager list comprehensions for memory-efficient iteration over large streams.
- **Context Managers**: Always manage I/O resources using `with` statements (`with open(...) as f:`).

---

## 3. Formatting & Linting Tooling
- **Ruff & Black**: Use Ruff for ultra-fast linting and Black/Ruff-format for deterministic code formatting.
- **Line Length**: Target standard 88 or 100 character line limits.
- **Naming Conventions**:
  - `snake_case`: Variables, functions, methods, modules.
  - `PascalCase`: Classes, Exceptions, Pydantic models.
  - `UPPER_SNAKE_CASE`: Constants.

---

## 4. Error Handling & Exceptions
- **Specific Exceptions**: Never catch bare `except:`. Catch specific exceptions (`except (ValueError, KeyError) as e:`).
- **Custom Exceptions**: Derive domain errors from a custom base exception class (`class DomainError(Exception): pass`).
- **Exception Chaining**: Use `raise NewException(...) from original_err` to preserve stack traces.

