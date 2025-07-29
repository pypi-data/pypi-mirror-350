"""
Use case decorator implementation with transactional tracing support.

This module provides a flexible decorator `@use_case` that can be used with or
without parentheses. It wraps a function with transaction lifecycle management,
based on globally available tracing and transaction managers.

Functions decorated will be marked with `__is_use_case__ = True` and traced
automatically using the configured system.

To enable function signature preservation for autocompletion and static analysis
(especially in Python < 3.10), it is recommended to install `typing_extensions`.

Installation
------------
pip install typing_extensions
"""
import inspect
from functools import wraps
from typing import Optional, Union, Callable, Tuple

from ..ports.tracing.opener_tracer import OpenerTracer
from ..domain_context import domain_context
from ..transactional.transaction_manager import transaction_manager, TransactionManager
from ..utils.is_free_function import is_free_function
from ..typing_compat import P, R, ParamSpec

tracing_opener = domain_context.opener


def _prepare_function(fn: Callable, keyname: Optional[str], do_trace: bool) -> Tuple[str, bool]:
    """Prepares the function for use case decoration.

    Parameters
    ----------
    fn : Callable
        The function to decorate.
    keyname : Optional[str]
        The keyname for tracing, or None to use the function name.
    do_trace : bool
        Whether tracing is enabled.

    Returns
    -------
    Tuple[str, bool]
        The resolved keyname and whether the function accepts a transaction_id.
    """
    m_keyname = keyname or fn.__name__
    sig = inspect.signature(fn)
    accepts_transaction_id = (
            do_trace and
            ("transaction_id" in sig.parameters
             or any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values()))
    )
    if is_free_function(fn):
        fn.__is_use_case__ = True
    return m_keyname, accepts_transaction_id


def _run_with_trace(
        fn: Callable[..., R],
        args: tuple,
        kwargs: dict,
        keyname: str,
        do_trace: bool,
        *,
        _tracing_opener: OpenerTracer,
        _transaction_manager: TransactionManager,
        _accepts_transaction_id: bool) -> R:
    """
    Executes a function with transactional tracing logic.

    Handles transaction start, end, and error tracing transparently.

    Parameters
    ----------
    fn : Callable
        The original use case function to invoke.
    args : Any
        Positional arguments to pass to the function.
    kwargs : dict
        Keyword arguments to pass to the function.
    keyname : str
        The keyname used for transaction and component tracing.
    do_trace : bool
        Whether to enable tracing or not.
    _tracing_opener : Any
        The global tracing system opener.
    _transaction_manager : Any
        The global transaction manager.

    Returns
    -------
    R
        The result of the function call.

    Raises
    ------
    BaseException
        If the function raises an exception, it is traced and re-raised.
    """
    super_transaction_id = kwargs.pop("transaction_id", None)
    transaction_id = super_transaction_id

    if do_trace:
        transaction_id = _transaction_manager.create_transaction_id(keyname)
        _tracing_opener.start(*args,
                              super_transaction_id=super_transaction_id,
                              component=keyname,
                              transaction_id=transaction_id,
                              **kwargs)

    if super_transaction_id is None:
        super_transaction_id = transaction_id

    try:
        if _accepts_transaction_id:
            result = fn(*args, transaction_id=transaction_id, **kwargs)
        else:
            result = fn(*args, **kwargs)
    except BaseException as ex:
        if do_trace:
            _tracing_opener.end(
                transaction_id=transaction_id,
                component=keyname,
                super_transaction_id=super_transaction_id,
                result=ex,
            )
            _transaction_manager.close_transaction()
        raise

    if do_trace:
        _tracing_opener.end(transaction_id=transaction_id,
                            component=keyname,
                            super_transaction_id=super_transaction_id,
                            result=result)
        _transaction_manager.close_transaction()

    return result


if ParamSpec is not None:
    P = ParamSpec("P")


    def use_case(
            _fn: Optional[Callable[P, R]] = None,
            *,
            keyname: Optional[str] = None,
            do_trace: bool = True
    ) -> Union[Callable[P, R], Callable[[Callable[P, R]], Callable[P, R]]]:
        """
        Flexible use case decorator that supports usage with or without parentheses.

        Usage examples
        --------------
        @use_case
        def my_func(...): ...

        @use_case(keyname="custom", do_trace=False)
        def my_func(...): ...

        Parameters
        ----------
        _fn : Callable, optional
            Internal-only argument. Do not pass manually.
        keyname : Optional[str], optional
            Tracing keyname. Defaults to the function name.
        do_trace : bool, optional
            Whether to trace the execution. Defaults to True.

        Returns
        -------
        Callable
            A function decorator or the decorated function, depending on usage.
        """

        def decorator(fn: Callable[P, R]) -> Callable[P, R]:
            m_keyname, accepts_transaction_id = _prepare_function(fn, keyname, do_trace)

            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return _run_with_trace(
                    fn, args, kwargs, m_keyname, do_trace,
                    _tracing_opener=tracing_opener,
                    _transaction_manager=transaction_manager,
                    _accepts_transaction_id=accepts_transaction_id
                )

            return wrapper

        if _fn is not None:
            return decorator(_fn)

        return decorator
else:
    def use_case(
            _fn: Optional[Callable[..., R]] = None,
            *,
            keyname: Optional[str] = None,
            do_trace: bool = True
    ) -> Union[Callable[..., R], Callable[[Callable[..., R]], Callable[..., R]]]:
        """
        Fallback version of the use_case decorator without signature preservation.

        This version is used when ParamSpec is not available.

        Parameters
        ----------
        _fn : Callable, optional
            Internal-only argument. Do not pass manually.
        keyname : Optional[str], optional
            Tracing keyname. Defaults to the function name.
        do_trace : bool, optional
            Whether to trace the execution. Defaults to True.

        Returns
        -------
        Callable
            A function decorator or the decorated function, depending on usage.
        """

        def decorator(fn: Callable[..., R]) -> Callable[..., R]:
            m_keyname, accepts_transaction_id = _prepare_function(fn, keyname, do_trace)

            @wraps(fn)
            def wrapper(*args, **kwargs) -> R:
                return _run_with_trace(
                    fn, args, kwargs, m_keyname, do_trace,
                    _tracing_opener=tracing_opener,
                    _transaction_manager=transaction_manager,
                    _accepts_transaction_id=accepts_transaction_id
                )

            return wrapper

        if _fn is not None:
            return decorator(_fn)

        return decorator
