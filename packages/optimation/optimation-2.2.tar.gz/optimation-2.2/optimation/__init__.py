"""
Optimation 2.1 Enhanced: Includes optimate, quantum logic, and modeling interface.
"""
from .core import optimate
from .logic import balance_variables, exponential_weighting
from .quantum import quantum_weight_adjustment, quantum_superposition
from .model import Variable, Model, Objective
from .solver import minimize

__version__ = '2.1'
