# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict data structures."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal, NoReturn, TypeVar, cast, overload

from docplex.mp.dvar import Var
from docplex.mp.linear import LinearExpr, ZeroExpr
from docplex.mp.model import Model
from docplex.mp.vartype import VarType

from ._dict_mixins import DefaultT, Dict1DMixin, DictBaseMixin, DictNDMixin
from ._index_sets import Elem1DT, ElemNDT, ElemT, IndexSet1D, IndexSetBase, IndexSetND

VarT = TypeVar('VarT', bound=Var)


class VarDictBase(dict[ElemT, VarT], DictBaseMixin[ElemT, VarT]):
    """Base class for custom subclasses of `dict` to define DOcplex model variables.

    Provides:
    1. Runtime type checks to ensure variables are `docplex.mp.dvar.Var` objects.
    2. Disables all mutable mapping operations.

    Parameters
    ----------
    docpx_var_dict : dict
        Dictionary of variable objects from docplex.
    indexset : IndexSetBase
        Keys of dictionary encapsulated in an IndexSet.
    model : docplex.mp.model.Model
        DOcplex model associated with the variable objects.
    vartype : docplex.mp.vartype.VarType
        DOcplex VarType corresponding to the variable objects.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetBase
    #     Index-set of keys.

    __slots__ = ('_indexset', '_model', '_vartype')

    def __init__(
        self,
        docpx_var_dict: dict[ElemT, VarT],
        /,
        *,
        indexset: IndexSetBase[ElemT],
        model: Model,
        vartype: VarType,
    ) -> None:
        self._validate_docpx_var_dict(docpx_var_dict)

        if indexset._set != set(docpx_var_dict.keys()):
            raise ValueError(
                f'{indexset.__class__.__name__} elements and {self.__class__.__name__} keys are not'
                ' the same.'
            )

        self._indexset = indexset
        """Index-set of keys."""

        self._model = model
        self._vartype = vartype

        super().__init__(docpx_var_dict)

    @property
    def model(self) -> Model:
        """DOcplex model associated with the variables.

        Returns
        -------
        docplex.mp.model.Model
        """
        return self._model

    @property
    def vartype(self) -> VarType:
        """DOcplex VarType corresponding to the variables.

        Returns
        -------
        DOcplex variable type (subclass of docplex.mp.vartype.VarType)
        """
        return self._vartype

    @staticmethod
    def _validate_docpx_var_dict(docpx_var_dict: dict[ElemT, VarT]) -> None:
        """Validate that the input is a populated dict of DOcplex variables.

        Parameters
        ----------
        docpx_var_dict : dict
            Input dictionary for VarDict.
        """
        if not isinstance(docpx_var_dict, dict):
            raise TypeError('input should be a dict')
        if not docpx_var_dict:
            raise ValueError('dict should be populated')
        if any(not isinstance(x, Var) for x in docpx_var_dict.values()):
            raise TypeError('dict values should be docplex.mp.dvar.Var objects')

    def __setitem__(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__setitem__')

    def __delitem__(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('__delitem__')

    def clear(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('clear')

    def copy(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('copy')

    @overload
    def get(self, key: ElemT, /) -> VarT | None: ...  # numpydoc ignore=GL08

    @overload
    def get(self, key: ElemT, default: DefaultT, /) -> VarT | DefaultT: ...  # numpydoc ignore=GL08

    def get(self, key: ElemT, default: DefaultT | None = None, /) -> VarT | DefaultT | None:
        """Get the variable for the specified key, or the default if not found.

        Parameters
        ----------
        key : key
        default : Any, optional

        Returns
        -------
        docplex.mp.dvar.Var or ``default``
        """
        return super().get(key, default)

    def pop(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('pop')

    def popitem(self) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('popitem')

    def setdefault(self, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('setdefault')

    def update(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Not supported by VarDict."""
        self._raise_not_supported_err('update')

    @classmethod
    def fromkeys(cls, *args: Any) -> NoReturn:
        """Not supported by VarDict."""
        raise AttributeError(f'`fromkeys` is not supported by {cls.__name__}')


class VarDict1D(VarDictBase[Elem1DT, VarT], Dict1DMixin[Elem1DT, VarT]):
    """Custom subclasses of `dict` to define DOcplex model variables with 1-dim scalar keys.

    Parameters
    ----------
    docpx_var_dict : dict
        Dictionary of variable objects from docplex.
    indexset : IndexSet1D
        Keys of dictionary encapsulated in IndexSet1D.
    model : docplex.mp.model.Model
        DOcplex model associated with the variable objects.
    vartype : docplex.mp.vartype.VarType
        DOcplex VarType corresponding to the variable objects.
    value_name : str, optional
        Name to refer to variables - not used internally, and solely for user reference.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSet1D
    #     Index-set of keys.

    __slots__ = ('_key_name', '_value_name')

    def __init__(
        self,
        docpx_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> None:
        self.key_name = indexset.name
        self.value_name = value_name

        super().__init__(docpx_var_dict, indexset=indexset, model=model, vartype=vartype)

    def __new__(
        cls,
        docpx_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDict1D is built through the '
            'docplex_extensions.add_variables function'
        )

    @classmethod
    def _create(
        cls,
        docpx_var_dict: dict[Elem1DT, VarT],
        indexset: IndexSet1D[Elem1DT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> VarDict1D[Elem1DT, VarT]:
        # Private method to construt VarDict1D
        instance = super().__new__(cls)
        cls.__init__(
            instance, docpx_var_dict, indexset, model=model, vartype=vartype, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p, cycle: bool) -> None:  # type: ignore[no-untyped-def]
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        # Since IPython is not typed, we'll add a type ignore commnent here
        # The annotation for arg `p` is `IPython.lib.pretty.RepresentationPrinter`
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, key: Elem1DT) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        key : key

        Returns
        -------
        docplex.mp.dvar.Var or ``0``

        Examples
        --------
        Create DOcplex model:

        >>> from docplex.mp.model import Model
        >>> mdl = Model()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from docplex_extensions import add_variables
        >>> node_select = add_variables(mdl, nodes, 'B', name='node-select')

        Lookup for keys:

        >>> node_select.lookup('A')
        docplex.mp.Var(type=B,name='node-select_A')

        >>> node_select.lookup('Z')
        0
        """
        return super().get(key, 0)

    def sum(self) -> LinearExpr | ZeroExpr:
        """Sum all variables in a linear expression.

        Returns
        -------
        docplex.mp.linear.LinearExpr or docplex.mp.linear.ZeroExpr

        Examples
        --------
        Create DOcplex model:

        >>> from docplex.mp.model import Model
        >>> mdl = Model()

        Create index-set:

        >>> nodes = IndexSet1D(['A', 'B', 'C'], name='node')

        Add variables:

        >>> from docplex_extensions import add_variables
        >>> node_select = add_variables(mdl, nodes, 'B', name='node-select')

        Sum all variables:

        >>> node_select.sum()
        docplex.mp.LinearExpr(node-select_A+node-select_B+node-select_C)
        """
        return self.model.sum_vars_all_different(self.values())


class VarDictND(VarDictBase[ElemNDT, VarT], DictNDMixin[ElemNDT, VarT]):
    """Custom subclasses of `dict` to define DOcplex model variables with N-dim tuple keys.

    Parameters
    ----------
    docpx_var_dict : dict
        Dictionary of variable objects from docplex.
    indexset : IndexSetND
        Keys of dictionary encapsulated in IndexSetND.
    model : docplex.mp.model.Model
        DOcplex model associated with the variable objects.
    vartype : docplex.mp.vartype.VarType
        DOcplex VarType corresponding to the variable objects.
    value_name : str, optional
        Name to refer to variables - not used internally, and solely for user reference.
    """

    # Private attributes
    # ------------------
    # _indexset : IndexSetND
    #     Index-set of keys.

    __slots__ = ('_key_names', '_value_name')

    def __init__(
        self,
        docpx_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> None:
        self.key_names = indexset.names
        self.value_name = value_name

        super().__init__(docpx_var_dict, indexset=indexset, model=model, vartype=vartype)

    def __new__(
        cls,
        docpx_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        raise TypeError(
            'This class is not meant to be instantiated; VarDictND is built through the '
            'docplex_extensions.add_variables function'
        )

    @classmethod
    def _create(
        cls,
        docpx_var_dict: dict[ElemNDT, VarT],
        indexset: IndexSetND[ElemNDT],
        /,
        *,
        model: Model,
        vartype: VarType,
        value_name: str | None = None,
    ) -> VarDictND[ElemNDT, VarT]:
        # Private method to construt VarDictND
        instance = super().__new__(cls)
        cls.__init__(
            instance, docpx_var_dict, indexset, model=model, vartype=vartype, value_name=value_name
        )
        return instance

    def __repr__(self) -> str:
        # Printable string representation.
        return f'{self._get_repr_header()}\n{super().__repr__()}'

    def _repr_pretty_(self, p, cycle: bool) -> None:  # type: ignore[no-untyped-def]
        # Pretty repr for IPython.
        # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
        # Since IPython is not typed, we'll add a type ignore commnent here
        # The annotation for arg `p` is `IPython.lib.pretty.RepresentationPrinter`
        p.text(f'{self._get_repr_header()}\n')
        p.pretty(dict(self))

    def lookup(self, *key: Any) -> VarT | Literal[0]:
        """Get the variable for the specified key, or zero if it is not found.

        Parameters
        ----------
        *key : key

        Returns
        -------
        docplex.mp.dvar.Var or ``0``

        Examples
        --------
        Create DOcplex model:

        >>> from docplex.mp.model import Model
        >>> mdl = Model()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from docplex_extensions import add_variables
        >>> arc_flow = add_variables(mdl, arcs, 'C', ub=10, name='arc-flow')

        Lookup with keys:

        >>> arc_flow.lookup('A', 'B')
        docplex.mp.Var(type=C,name='arc-flow_A_B',ub=10)

        >>> arc_flow.lookup('X', 'Y')
        0
        """
        if any((isinstance(k, Iterable) and not isinstance(k, str)) for k in key):
            raise TypeError('lookup key must be scalars (no iterables except string)')
        if len(key) != self._indexset._tuplelen:
            raise ValueError('lookup key length must be the same as that of N-dim tuple keys')
        return super().get(cast('ElemNDT', key), 0)

    def sum(self, *pattern: Any) -> LinearExpr | ZeroExpr:
        """Sum all variables, or a subset based on wildcard pattern, in a linear expression.

        Parameters
        ----------
        *pattern : Any, optional
            For subsets, the pattern requires one value for each dimension of the N-dim tuple key.
            The single-character string ``'*'`` (asterisk) can be used as a wildcard to represent
            all possible values for a dimension.

        Returns
        -------
        docplex.mp.linear.LinearExpr or docplex.mp.linear.ZeroExpr

        Raises
        ------
        TypeError
            If the pattern includes non-scalar(s).
        ValueError
            If the pattern is not the same as the length of N-dim tuple keys.
        ValueError
            If the pattern has no wildcard or all wildcards.

        Examples
        --------
        Create DOcplex model:

        >>> from docplex.mp.model import Model
        >>> mdl = Model()

        Create index-set:

        >>> arcs = IndexSetND([('A', 'B'), ('B', 'C'), ('C', 'B')], names=['ori', 'des'])

        Add variables:

        >>> from docplex_extensions import add_variables
        >>> arc_flow = add_variables(mdl, arcs, 'C', ub=10, name='arc-flow')

        Sum all variables:

        >>> arc_flow.sum()
        docplex.mp.LinearExpr(arc-flow_A_B+arc-flow_B_C+arc-flow_C_B)

        Sum subset of variables having ``'B'`` at the second dimension index:

        >>> arc_flow.sum('*', 'B')
        docplex.mp.LinearExpr(arc-flow_A_B+arc-flow_C_B)

        Sum subset of variables having ``'Z'`` at the first dimension index:

        >>> arc_flow.sum('Z', '*')
        docplex.mp.ZeroExpr()
        """
        if pattern:
            return self.model.sum_vars_all_different(self.subset_values(*pattern))
        return self.model.sum_vars_all_different(self.values())
