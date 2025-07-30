# mbls

A Python toolkit for **Model-Based Local Search** algorithm design.

Built on top of [Routix](https://pypi.org/project/routix/),
it provides a modular framework for orchestrating subroutines, managing experimental runs, and integrating mathematical models into heuristic search routines.

## Features

- **Modular Architecture**
  Compose and extend LNS-style strategies using reusable subroutine components.
- **Seamless Routix Integration**
  Take advantage of structured routine execution, logging, timers, and experiment summarization.
- **Extensible Modeling Layer**
  Easily add custom models, constraints, or solvers.

✅ Includes support for OR-Tools CP-SAT via `mbls.cpsat`.

## Installation

```sh
pip install mbls
```

## Requirements

- routix (experiment orchestration)
- ortools (for `mbls.cpsat` components)

## 🚀 Example

```python
from mbls.cpsat import CustomCpModel

# Initialize model
model = CustomCpModel()

# Define variables, constraints, and objective
# ...

# Configure and solve
model.init_solver(computational_time=10.0, n_threads=4)
status, elapsed, ub, lb = model.solve_and_get_status(10.0, 4)

print(f"Status: {status}, UB: {ub}, LB: {lb}")
```

## 🧩 Extendability

`mbls` is designed for research and experimentation. You can:

- Subclass `SubroutineController` to define custom LNS or hybrid metaheuristics
- Extend `CustomCpModel` to support new problem domains
- Compose repeatable flows with structured routine names and modular inputs

## License

MIT License
