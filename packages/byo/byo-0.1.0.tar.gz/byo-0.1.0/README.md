# byo

A simple decorator to benchmark functions.

## Installation

```shell
pip install byo
```

## Usage

Just import the `bench` decorator and apply it to any function you want to benchmark!

```python
from byo import bench

@bench
def benchmarked_function():
  ...
```

The decorator registers an `atexit` callback to print a report of function calls when the program finishes.

## Example

Say we want to benchmark how long it takes to read and write some text to a file. We can use the `bench` decorator on those functions to profile them as follows.

```python
from byo import bench

@bench
def read_file():
  with open("lorem.txt", "r") as f:
    f.read()

@bench
def write_file(text: str):
  with open("lorem.txt", "w") as f:
    f.write(text)

f = open("lorem.txt", "r")
LOREM = f.read()
f.close()

N = 1000

for _ in range(N):
  read_file()

for _ in range(N):
  write_file(LOREM)
```

Running this should output something like:
```shell
=== Report ===
| Function   |   Calls |   Average (ms) |   Median (ms) |   Min (ms) |   Max (ms) |
|------------|---------|----------------|---------------|------------|------------|
| read_file  |    1000 |         0.0101 |        0.0092 |     0.0074 |     0.1033 |
| write_file |    1000 |         0.0326 |        0.0283 |     0.0224 |     1.0325 |
```

More examples can be found in [/examples](examples/).
