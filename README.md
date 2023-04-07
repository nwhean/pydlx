# PyDLX

## Description

A Python implementation of Donald Knuth's Dancing Link Algorithm.

## Getting Started

### Dependencies

* Python 3.9 or above.

### Installing

* pip install git+https://github.com/nwhean/pydlx.git

### Executing program

* Import the required functions
```py
from pydlx import create_matrix, search, print_solution
```

* Create a dancing link network with exact cover matrix. `names` is optional, and if not given, defaults to integer index starting from 0.
```py
root = create_network([
            [0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 1]],
            names=["A", "B", "C", "D", "E", "F", "G"])
```

* The `search` function returns a generator of solution set to the exact cover problem. It is possible to iterate through all the solutions as such:
```py
for solution in search(root):
    print_solution(solution)
```

* With the example exact cover matrix given, the following will be printed out. Note that the row sequence or the sequece within the row.
```
A D
E F C
B G

```

## Author

* Wee Hean Ng

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

References were made to the following materials
* [Dancing Links](https://arxiv.org/abs/cs/0011047)
