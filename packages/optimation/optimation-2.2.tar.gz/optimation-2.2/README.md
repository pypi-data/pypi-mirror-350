# Optimation v2.2

A flexible framework for variable weighting, quantum-inspired logic, and simplified modeling.

## Features
- Variable Weighting
- Exponential/Quantum Logic
- Modeling: Variables, Objectives, Minimization

## Example

```python
from optimation import Variable, Model, Objective, minimize

x = Variable("x", 10)
y = Variable("y", 20)

def total(vars): return sum(v.value for v in vars)

model = Model()
model.add_variable(x)
model.add_variable(y)
model.add_objective(Objective(total))

print(minimize(model))
```
