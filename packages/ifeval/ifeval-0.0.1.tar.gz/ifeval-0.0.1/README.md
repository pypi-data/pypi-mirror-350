# ifeval

**Evaluate all `if`-statement predicates in a Python file and simplify the code by removing unreachable branches.**

This tool parses a Python source file, evaluates constant `if` conditions (`if f(x)`, `if x is None`, etc.), and rewrites the file to include only the branches that would execute.

---

## Installation

Clone the repository and install with pip:

```bash
git clone https://gitlab.com/knvvv/ifeval.git
cd ifeval
pip install .
```

## Usage

### Dry run (default)

To preview changes without modifying the file:

```bash
ifeval path/to/your_script.py
```

It will print the diff showing what would be changed.

### Apply changes

To actually rewrite the file in-place, add the --no-dry flag:

```bash
ifeval path/to/your_script.py --no-dry
```

## Example
Given the following code:

```python
print("Hello")
if True:
    print("Keep this")
else:
    print("Remove this")
```

`ifeval` simplifies it to:

```python
print("Hello")
print("Keep this")
```

## ⚠️ **A word of caution** ⚠️

This package executes all the code from files being analyzed. **Do not run it on untrusted or potentially malicious code**, as it may lead to arbitrary code execution.
