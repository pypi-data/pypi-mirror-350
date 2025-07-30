# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
The `docplex-extensions` package.

A collection of custom data structures and user-friendly functions for mathematical optimization
modeling with DOcplex — IBM® Decision Optimization CPLEX® Modeling for Python.
"""

__version__ = '1.3.1'

# Check required dependencies
from importlib.util import find_spec as _find_spec

if _find_spec('docplex') is None:
    raise ImportError('Unable to import required dependency: docplex')

# Package functionality
from ._index_sets import IndexSet1D, IndexSetND
from ._model_funcs import print_problem_stats, print_solution_quality_stats, runseeds, solve
from ._pandas_accessors import DataFrameAccessor as _DataFrameAccessor
from ._pandas_accessors import IndexAccessor as _IndexAccessor
from ._pandas_accessors import SeriesAccessor as _SeriesAccessor
from ._param_dicts import ParamDict1D, ParamDictND
from ._tuning_funcs import batch_tune, tune
from ._var_dicts import VarDict1D, VarDictND
from ._var_funcs import add_variable, add_variables

# Register custom accessors if pandas is available
try:
    import pandas as _pd

    _pd.api.extensions.register_series_accessor('dex')(_SeriesAccessor)
    _pd.api.extensions.register_dataframe_accessor('dex')(_DataFrameAccessor)
    _pd.api.extensions.register_index_accessor('dex')(_IndexAccessor)

except ImportError:
    pass

# Public API
__all__ = [
    'print_problem_stats',
    'print_solution_quality_stats',
    'solve',
    'tune',
    'batch_tune',
    'runseeds',
    'IndexSet1D',
    'IndexSetND',
    'ParamDict1D',
    'ParamDictND',
    'VarDict1D',
    'VarDictND',
    'add_variable',
    'add_variables',
]
