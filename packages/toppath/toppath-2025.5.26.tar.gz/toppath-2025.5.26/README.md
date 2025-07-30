# toppath

a package on top of pathlib and path to use path easily

## installation

```bash
pip install toppath
```

## usage

```python
from toppath.path import Path

d = Path("hello.txt")
print(d.exists())

# d.pp is pathlib.Path object
print(d.pp)

```
