# QEC Bivariate Bicycle Codes

A Python package for quantum error correction using bivariate bicycle codes.

## Installation

```bash
pip install bbqec
```

## Usage

### Basic Usage Example

```python
from bbqec import BBCode

# Create a new BBCode
l = 8
m = 10
A = ['i', 'x1', 'y7', 'x6.y5']
B = ['x0', 'x5', 'y6.x7', 'x.y5']

code = BBCode(l, m, A, B)

# Find the parameters of the code
# distance_method = 4 uses bposd to calculate the distance (recommended)
n, k, d = code.generate_bb_code(distance_method=4)
print(f"Code parameters: [{n}, {k}, {d}]")

# Get parity-check matrices
H_x, H_z = code.create_parity_check_matrices()

# Create Tanner Graph
G = code.make_graph()
```

### Optimized Version for Multiple Codes

```python
from bbqec import BBCodeOptimised
from bbqec.helpers import ProposeParameters

# Set up parameters
l = 10
m = 8
num_codes = 50

# Create an instance of BBCodeOptimised
code = BBCodeOptimised(l, m)

# Help generate random A and B expressions
parameters = ProposeParameters(l, m)

# Generate codes
for _ in range(num_codes):
    A = parameters.draw_bivariate_monomials(num_monomials=3)
    B = parameters.draw_bivariate_monomials(num_monomials=3)
    
    code.set_expressions(A_expression=A, B_expression=B)
    n, k, d = code.find_distance(distance_method=4)
    
    print(f"Code parameters: [{n}, {k}, {d}]")
```

## Documentation

For detailed documentation, usage examples, and more information about the API:

*   Visit the [GitHub repository](https://github.com/vanshjjw/qec-bivariate-bicycle).
*   Check out the [Usage Guide (src/usage.md)](https://github.com/vanshjjw/qec-bivariate-bicycle/blob/master/src/usage.md).

## Features

*   Create and analyze bivariate bicycle quantum error correction codes
*   Multiple distance calculation methods
*   Optimized implementations for generating multiple codes
*   Tanner graph representation of codes
*   Polynomial helpers for working with bivariate polynomials
