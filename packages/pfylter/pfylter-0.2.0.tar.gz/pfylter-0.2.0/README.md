# 🔍 pfylter

**pfylter** is a lightweight, flexible, and extensible Python framework for applying composable filters to arbitrary data. It’s built using the **composite design pattern**, allowing complex logical conditions to be expressed and reused cleanly.

---

## 🚀 Features

- ✅ Define your own filters by subclassing `AbstractFilter`
- ✅ Combine filters using logical **AND** (`AllFilters`) or **OR** (`AnyFilter`)
- ✅ Support for generic data types (strings, numbers, objects, etc.)
- ✅ Clean, readable syntax using list comprehensions and type hints
- ✅ Perfect for data processing, rule engines, and validation pipelines

---

## 📦 Installation

```bash
pip install pfylter
```

---

## ✨ Quick Start

### 1. Define Some Filters

```python
from pfylter import LenFilter, StartsWithFilter

data = ["A", "ABCD", "B", "BCDE", "C", "AAAAAAA"]

# Only keep strings of length 4 that start with 'A'
from pfylter import AllFilters

f = AllFilters([
    LenFilter(4),
    StartsWithFilter("A")
])

print(f.apply(data))  # ['ABCD']
```

---

### 2. Use OR Logic with `AnyFilter`

```python
from pfylter import AnyFilter

f = AnyFilter([
    LenFilter(4),
    StartsWithFilter("A")
])

print(f.apply(data))  # ['A', 'ABCD', 'BCDE', 'AAAAAAA']
```

---

## 🔄 Composing Filters

Because `AllFilters` and `AnyFilter` are themselves filters, they can be **nested** to build complex conditions:

```python
from pfylter import AllFilters, AnyFilter, LenFilter, StartsWithFilter

# Keep strings that start with 'A' and have length 1 or 4
complex_filter = AllFilters([
    StartsWithFilter("A"),
    AnyFilter([
        LenFilter(1),
        LenFilter(4)
    ])
])

print(complex_filter.apply(["A", "ABCD", "AAAAAA", "B"]))  # ['A', 'ABCD']
```

---

## 🛠 Creating Custom Filters

You can define custom filters by inheriting from `AbstractFilter`:

```python
from pfylter import AbstractFilter

class GreaterThanFilter(AbstractFilter[int]):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def keep(self, instance: int) -> bool:
        return instance > self.threshold
```

Now you can use this filter in combination with others!

---

## 📝 License

MIT License — see `LICENSE` file for details.

---

## 🤝 Contributing

Feel free to open issues or pull requests. All feedback is welcome!
