# shansort

## What is Shan Sort?

Shan Sort is a stable and efficient radix sorting algorithm implemented in C. It sorts 64-bit integers by processing their binary digits (bits) in passes, making it faster than traditional comparison-based sorts for large datasets. It also handles negative numbers by offsetting them during sorting.

---

## How to Use

After installing the package, you can import and use the sorting function like this:

```python
from shansort import shan_sort

data = [10, -5, 3, 0, -2]
sorted_data = shan_sort(data)
print(sorted_data)  # Output: [-5, -2, 0, 3, 10]
