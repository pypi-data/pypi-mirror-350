# pyccb
Python Compiler Collection for Bash

## What is it
`pyccb` is a Python -> Pure Bash compiler. It can be used for anything, like making your bash scripts in a more familiar language or running your Python scripts in Bash for fun!

## How to use it
`pyccb` can be used as a CLI or as a Python package.

**Installation:**
```bash
# In the cloned repository
pip install -e .
```

**CLI Usage:**
```bash
pyccb -h
```
```bash
pyccb examples/helloworld.py -o helloworld.sh
```

**Python Package Usage:**
```py
import pyccb

pyccb.compile("print ('Hello World')")
```

## Features + Guide
`pyccb` supports only a small subset of the full Python syntax. Currently it supports

- Integer Types
- String Types
- Variable declarations
- Function calls (with parameters)
- Basic arithmatic (+-*/)
- Conditionals + `if` statements
- `while` Loops

To make your program useful, you can call commands as normal functions. eg.
```py
echo("Hello World")
```

See `examples/` for more usage examples. You can compile all the examples by running `./tests/all.sh`.

## License
This repository is licensed under the GNU General Public License V3

```
simplyrohan/pyccb - Python Compiler Collection for Bash
Copyright (C) 2025 simplyrohan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```