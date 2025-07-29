""" Copyright 2025 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import threading
from textwrap import dedent as text_dedent
from textwrap import indent as text_indent

import numba
import numpy
import sympy
from sympy.utilities.lambdify import MODULES as lambdify_modules

from .config import (
    DTYPES_FILLER_HINT,
    SYMPY_ATOMS_FP,
    UNSET,
)
from .data import dtype_result_guess

from .messaging import warn


def signature_automatic(expr, data, indexers=None, name_result=None):
    """ generate signature via naive Numba build """

    # TODO consider erroring if self-referential "r[n] = a[n] + r[n-1]"
    #   user must provide partially-filled result array, so type is already known
    #   still, this could warn them the type isn't what Numba expected

    # FIXME also verify with a given result_type?
    # FUTURE do safe casts and warn at completion?

    # remove indexing from the expr to avoid issues with basic lambdify
    if indexers:
        if len(indexers) != 1:
            raise ValueError("BUG: only a single indexer allowed if provided")
        indexer, (start, end) = next(iter(indexers.items()))
        slice_start = end - start      # start where values are likely to be valid
        slice_end   = slice_start + 1  # slice should always be [n:n+1]
        # NOTE checked during row build if this overruns the data `[1,2,3][5:6]` -> `[]`

        # trade all the indexed symbols (IndexedBase) for a direct Symbol
        replacements        = {}
        replacement_symbols = {}  # keep multiple instances consistent
        for atom in expr.atoms(sympy.Indexed):
            name = atom.atoms(sympy.IndexedBase).pop().name  # `a[i+1]` -> `"a"`
            try:
                sub_sym = replacement_symbols[name]
            except KeyError:
                sub_sym = sympy.Symbol(name)
                replacement_symbols[name] = sub_sym
            replacements[atom] = sub_sym
        expr = expr.subs(replacements)
    else:
        slice_start = None
        slice_end   = 1

    # FIXME this doesn't always work, especially when a result array is passed
    #   this is generally still part of [ISSUE 79] (see assorted follow-ups)
    # clobber expr with an equivalent one
    expr = expr.rhs
    args = sorted(s.name for s in expr.free_symbols)  # lexical sort matches other parses
    # if name_result is not None and name_result in data:
    #     args.append(name_result)
    #     expr = expr - sympy.Symbol(name_result)

    # make a new data table as if it only had 1 row, maintaining the inner shape and types
    data_1row = {}
    for name in args:  # avoids unused keys in data
        ref = data[name]
        if ref.ndim == 0:
            value = ref
        else:
            value = ref[slice_start:slice_end]
            if len(value) != 1:
                raise ValueError(f"data[{name}] with shape {ref.shape} doesn't have enough data to match combined offset({slice_start})")
        data_1row[name] = value

    # build callable and call it on single row
    fn = sympy.lambdify(args, expr)
    fn_jit = numba.jit(nopython=True)(fn)
    fn_jit(**data_1row)  # dynamic compile generates signature as a property
    # NOTE result ignored and might be [NaN], but the type and inner shape should be right

    # now extract signature
    count_signatures = len(fn_jit.nopython_signatures)
    if count_signatures != 1:  # should be impossible
        raise RuntimeError(f"BUG: unexpected signature count {count_signatures}: {fn_jit.nopython_signatures}")
    signature    = fn_jit.nopython_signatures[0]
    dtype_result = signature.return_type
    # coerce to NumPy type NOTE discards alignment
    dtype_result = numpy.dtype(str(dtype_result.dtype))  # numba.from_dtype(numpy.dtype("dtype")) for inverse

    return fn_jit, signature, dtype_result


def signature_generate(symbols, results, data, dtype_result, config):
    """ generate a signature like
          `Array(int64, 1d, C)(Array(int64, 1d, C))`
        note that Arrays can be named and they begin with the name "array", which
          `repr()` -> `array(int64, 1d, C)`

        refer to Numba types docs and Numba Array(Buffer) classes for more details
          https://numba.readthedocs.io/en/stable/reference/types.html
    """
    # FUTURE support for names (mabye an upstream change to numba)
    #   likely further C-stlye like `void(int32 a[], int64 b)`
    # without names, the dtypes are positional, so ordering must be maintained
    # within logic that could reorder the arguments after fixing the signature!
    # however, when the user calls the Expressive instance,
    # data is passed as kwargs `fn(**data)` to the inner function
    mapper = []

    if len(results) != 1:
        raise RuntimeError("BUG: results symbols should have exactly 1 member: {results}")
    name_result   = next(iter(results.keys()))  # NOTE dict of len==1 if given
    result_passed = bool(name_result in data)  # directly check membership

    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)
    for name in names_symbols:  # use symbol ordering, not data ordering
        ref   = data[name]
        field = numba.typeof(ref)  # `numba.types.Array(dtype, dims, layout)` or scalar type
        mapper.append(field)

    # TODO consider warning the user that dummy symbols in the data won't be used
    # NOTE collection only contains symbols which are exclusively a dummy
    # dummy_symbols_in_data = {s.name for s in symbols_dummy if s.name in data}
    # if dummy_symbols_in_data:
    #     warn(f"dummy symbols in data will be ignored: {dummy_symbols_in_data}")
    # TODO warn or raise if not all data names used (+config) [ISSUE 43]
    #   len() is sufficient (KeyError earlier if fewer, but may wrap that too)

    # discover result array dimensions
    if result_passed:
        dims = set(data[name].ndim for name in names_symbols if (name != name_result and data[name].ndim != 0))
        ndim_result = data[name_result].ndim
        if dims:  # ignore special case where only single values were passed
            # if len(dims) != 1:
            #     warn(f"unequal data dimensions may result in an error: {dims}")
            if ndim_result not in dims:
                raise ValueError(f"result dimensions (ndim={ndim_result}) do not match inputs: {dims}")
    else:
        dims = set(data[name].ndim for name in names_symbols) - {0}
        if not dims:  # should be detected in `data_cleanup`
            raise RuntimeError("BUG: impossible code path reached, cannot determine result array length from input arrays")
        if len(dims) != 1:
            raise ValueError(f"couldn't determine result dimensions from data, please provide a result array: {dims}")
        ndim_result = dims.pop()

    # now build complete signature for Numba to compile
    # FUTURE consider support for additional dimensions in result
    dtype = getattr(numba.types, str(dtype_result))
    result_type = numba.types.Array(dtype, ndim_result, "C")
    # range offsets when using threadpool parallelizer
    if config["builder.parallel_model.native_threadpool"]:
        if not result_passed:  # result is always passed
            mapper.append(result_type)
        mapper.append(numba.types.int64)  # FUTURE is 2**(32-1) enough values to index any real array?
        mapper.append(numba.types.int64)  # FUTURE might pass data length around as some property too

    # FUTURE probably always `numba.void(*mapper)` and result is always passed by-ref
    return result_type(*mapper), result_passed


def breakout_Sum_to_loop(expr, symbols, indexers, results, name_result, data, config):
    """ better take on reducing Sum instances
    """
    if indexers or expr.atoms(sympy.Indexed):
        raise RuntimeError(f"BUG: escaped indexers (should be impossible): {indexers} vs {expr.atoms(sympy.Indexed)}")

    attempt_simplify      = config["translate_simplify.build.sum.try_algebraic_convert"]
    threaded_timeout_warn = config["translate_simplify.build.sum.threaded_timeout_warn"]

    # collection of `Sum()` instances to work with and replace
    exprs_sums = expr.atoms(sympy.Sum)

    if attempt_simplify:
        # FUTURE `.simplify()` (and `summation()`?) can take an indefinite amount of time, consider
        #  - simple timeout [ISSUE 99] (warn user might optimize, then continue with loop functions?)
        #    consider `fork()` or multiprocessing so `simplify()` can be killed after timeout
        #  - tuning `ratio` arg
        #  - additional custom heuristics for `measure`, perhaps just marking `Sum()`
        if threaded_timeout_warn:
            # FUTURE warn for each `sum_block()` so with several the problematic one can be identified
            def watcher_simplify_warn(e, timeout):
                e.wait(timeout)
                if not e.is_set():
                    warn(
                        f"failed to simplify a Sum() instance in expr after {timeout}s"
                        " perform algebraic expand before .build()ing or set or pass config property"
                        " config['translate_simplify.build.sum.try_algebraic_convert']=False to force "
                        " loop codegen path if operation hangs indefinitely"
                    )

            event_watcher  = threading.Event()
            thread_watcher = threading.Thread(target=watcher_simplify_warn, args=(event_watcher, threaded_timeout_warn), daemon=True)
            thread_watcher.start()

        for sum_block in exprs_sums:
            sum_evaluated = sum_block.replace(sympy.Sum, sympy.summation)
            if not sum_evaluated.atoms(sympy.Sum):  # successfully decomposed `Sum()`
                # attempt to simplify numeric intermediates if any floating-point Atoms are used
                # as the result will be a Float and ideally the precision will remain the same
                #   >>> e = parse_expr("Sum(log(x/b), (x,1,10))")
                #   >>> e.doit()  # more precise, but may require many operations
                #   log(1/b) + log(2/b) + log(3/b) + log(4/b) + log(5/b) + log(6/b) + log(7/b) + log(8/b) + log(9/b) + log(10/b)
                #   >>> e.doit().simplify()      # 10! already exceeds 2**16
                #   10*log(1/b) + log(3628800)
                #   >>> e.doit().simplify().n()  # simplified
                #   10.0*log(1/b) + 15.1044125730755
                # NOTE evaluated functions which simplify to a number become `Float`, so
                #   this won't affect the result dtype
                # FUTURE does this make sense to apply to all inputs?
                #   probably not, but some subset could benefit
                if sum_evaluated.atoms(*SYMPY_ATOMS_FP):
                    # FIXME function instead of method used to ease test mocks
                    sum_evaluated = sympy.simplify(sum_evaluated).n()
                if not sum_evaluated.atoms(sympy.Piecewise):  # FIXME just block Piecewise for now [ISSUE 111]
                    expr = expr.replace(sum_block, sum_evaluated)
                continue  # next sum_block

        if threaded_timeout_warn:
            event_watcher.set()
            thread_watcher.join()

        if not expr.atoms(sympy.Sum):  # successfully simplified all Sum() instances
            block_sum_functions = ""
            return expr, symbols, indexers, results, block_sum_functions

    # iterate to extract dummy vars and raise for problematic structures
    dummy_symbols = {}
    for sum_block in exprs_sums:
        fn_sum = sum_block.function
        limits = sum_block.limits  # tuple of tuples
        # separate and compare limit features
        dummy_var, limit_start, limit_stop = limits[0]

        # keep a collection of all dummy_symbols
        # TODO can this use `dummy_symbols_split()` result? (mostly avoiding KeyError from data[dummy])
        dummy_symbols[dummy_var.name] = dummy_var

    # define a new indexer
    # from string import ascii_lowercase as abcdefghijklmnopqrstuvwxyz
    # next(n for n in "abcdefghijklmnopqrstuvwxyz" if n not in symbols)
    for char_try in " abcdefghijklmnopqrstuvwxyz":
        indexer = f"idx_{char_try}".rstrip("_ ")  # "idx_ " -> "idx"
        if indexer not in symbols and indexer not in dummy_symbols:  # string compare
            indexer = sympy.Idx(indexer)  # prepare for mirroring
            break  # success: keep it for later
    else:  # didn't find any valid indexer
        raise ValueError(f"couldn't find a suitable indexer, all ascii lowercase characters used in expr: {symbols}")

    # identify and prepare to convert all vector/tensor Symbols to IndexedBase
    indexers.update({indexer: [0, 0]})  # always have 0 spread
    offset_values = {}
    indexed_variants = {}
    sum_functions = {}
    for name, symbol in symbols.items():
        if name in dummy_symbols:  # dummy members will redefined later
            # continue  # FUTURE nested Sum() instances probably need/support this
            raise RuntimeError(f"BUG: problematic ref is a Symbol and dummy var: {name}")
        base = sympy.IndexedBase(name)
        try:
            if data[name].ndim == 0:
                continue
        except KeyError as ex:       # might be the result name when not passed in data
            if name not in results:  # this should be impossible
                raise RuntimeError(f"BUG: unknown Symbol '{name}' not in data({data.keys()}): {repr(ex)}")
        offset_values[name]      = base
        indexed_variants[symbol] = sympy.Indexed(base, indexer)

    # TODO is it possible for there to be no offset_values?
    #   I think this can only happen if all values are singular and a result array is given
    #   otherwise no result length can be determined
    #   though it is possible for an individual `Sum()` to avoid having any

    # FUTURE support and reorder Sum instances to best order if they're nested (consider recursion too)
    #   trivially, maybe `sort()` where key is the count of Sum() atoms and then lexically?
    #   will this already handle outer dummy vars? probably

    # for each Sum(), create a new custom Function which simply iterates across each dummy in its range
    # sum_functions = {}  # FIXME moved above to inject converters for ndim=0 [ISSUE 120]
    mapper_new_Sum_functions = {}
    for index, sum_block in enumerate(exprs_sums):
        fn_sum = sum_block.function
        limits = sum_block.limits  # tuple of tuples
        dummy_var, limit_start, limit_stop = limits[0]

        # discover and fill arguments
        args = {s.name: s for s in fn_sum.atoms(sympy.Symbol) - {dummy_var}}
        args = {name: args[name] for name in sorted(args.keys())}  # rebuild in lexical order
        # complain about some edge cases
        set_symbols_inner = set(args.keys()) | {s.name for s in limit_start.atoms(sympy.Symbol)} | {s.name for s in limit_stop.atoms(sympy.Symbol)}
        if not set_symbols_inner:
            warn(f"Sum() has no non-dummy symbols (skipped simplification?): {sum_block}")
        if "rowscalar" in set_symbols_inner:
            raise NotImplementedError("BUG: the name literally 'rowscalar' is reserved in Sum() for now (to mangle or by-ref) [ISSUE 143]")

        # TODO consider crushing sum_block to be a safe name then collection + numbering
        # TODO prefix with 0 for length of exprs_sums
        fn_name = f"SumLoop{index}"

        result_dtype_sum = dtype_result_guess(fn_sum, data)  # returns a type like numpy.foo

        # TODO needs some careful analysis about `stop` vs `stop+1` syntax
        # NOTE Symbols are not replaced by IndexedBase instances yet and frozen as-is here
        T = f"""
        def {fn_name}(start, stop, {", ".join(args.keys())}):
            rowscalar = numpy.{str(result_dtype_sum)}(0)
            for {dummy_var} in range(start, stop+1):
                rowscalar += {fn_sum}
            return rowscalar
        """

        # NOTE start and end can independently be Symbol or numeric
        F = sympy.Function(fn_name)(limit_start, limit_stop, *args.values())
        sum_functions[F] = text_dedent(T)  # maps Function to per-row finalized string

        # create a new Function with indexed args which when embedded will refer to the new loop
        F_indexed = sympy.Function(F.name)(*map(
            lambda a: indexed_variants.get(a, a),
            (limit_start, limit_stop, *args.values())
        ))
        mapper_new_Sum_functions[sum_block] = F_indexed

    # make a single block of string functions to embed as closure(s)
    block_sum_functions = "\n".join(sum_functions.values())

    # rewrite each `Sum()` instance in expr with indexed versions with the new name
    for sum_block, F_new in mapper_new_Sum_functions.items():
        expr = expr.replace(sum_block, F_new)

    # update symbols and the result value
    symbols.update(offset_values)
    expr = expr.replace(results[name_result], sympy.Indexed(symbols[name_result], indexer))

    return expr, symbols, indexers, results, block_sum_functions


def discover_parallelization(data, config):
    """ determine if build should use `numba.prange` """
    if config["builder.parallel_model.native_threadpool"]:
        return False, True
    if config["builder.parallel_model.allow_prange"] is not UNSET:
        return config["builder.parallel_model.allow_prange"], False
    if max(d.ndim for d in data.values()) <= 1:  # at least shouldn't have broadcasting errors
        return True, False
    # internal threading can ignore some broadcasting errors (and more?) [ISSUE 145]
    return False, False


def loop_function_template_builder(expr, symbols, indexers, results, result_passed, dtype_result, data, config):
    """ generate environment and code to support the function
         - create namespace
         - fill template
         - exec() to generate the code
         - extract new function
    """

    # parallization features
    allow_prange, use_native_threadpool = discover_parallelization(data, config)

    # get ready to build the template (note dict of len==1)
    name_result = next(iter(results.keys()))

    if not expr.atoms(sympy.Sum):
        block_sum_functions = ""
    else:
        # experimental Sum removal
        expr, symbols, indexers, results, block_sum_functions = breakout_Sum_to_loop(
            expr,
            symbols,
            indexers,
            results,
            name_result,
            data,
            config,
        )

    # build namespace with everything needed to support the new callable
    # simplified version of sympy.utilities.lambdify._import
    _, _, translations, import_cmds = lambdify_modules["numpy"]
    expr_namespace = {"I": 1j}  # alt `copy.deepcopy(lambdify_modules["numpy"][1])`
    for import_line in import_cmds:
        exec(import_line, expr_namespace)
    # NOTE older SymPy versions may not have any translations at all
    #   while the latest seems to be just `{'Heaviside': 'heaviside'}`
    #   however, this is left as a trivial case for my multi-version build+test tool,
    #   which detects this as a line that is not run and has no other testing
    for sympyname, translation in translations.items():
        expr_namespace[sympyname] = expr_namespace[translation]

    # determine if range or prange should be used for outer loop
    # NOTE this causes the internal logic to use threads and can result in serious
    #   errors which are lost while still returning success!
    if allow_prange:
        exec("from numba import prange", expr_namespace)

    # construct further template components
    names_symbols = list(symbols.keys())
    if use_native_threadpool:  # always include result for native_threadpool
        names_symbols.append("_offset_start")
        names_symbols.append("_offset_end")
    elif not result_passed:
        # drop the result from arguments
        names_symbols.pop()

    block_args = ", ".join(names_symbols)

    # FUTURE manage this with uneven arrays if implemented [ISSUE 10]
    # NOTE this will use the first discovery it can as arrays all have the same length
    #   or will not pass `data_cleanup()`
    if result_passed:  # go ahead and use the passed array if possible
        name_size_symbol = name_result
    else:
        atom = sympy.IndexedBase if indexers else sympy.Symbol
        for symbol in expr.rhs.atoms(atom):
            name_symbol = symbol.name
            if name_symbol == name_result:  # result not passed so it can't be used (earlier check)
                continue  # pragma nocover FIXME ordering depends on hash seeding PYTHONHASHSEED
            name_size_symbol = name_symbol
            break
        else:  # this should have been verified in `data_cleanup()` or `verify_indexed_data_vs_symbols()`
            raise ValueError("BUG: couldn't determine size of result array, at least one symbol must be an array or pass a result array to fill")

    # prepare values to fill template
    if indexers:
        if result_passed or use_native_threadpool:
            block_result = ""  # if the result array is passed in, fill it by-index
        else:                  # without it, dynamically create an array of discovered length
            result_filler = DTYPES_FILLER_HINT[dtype_result]  # KeyError should be impossible
            block_result = f"{name_result} = numpy.full_like({name_size_symbol}, {result_filler}, dtype={dtype_result})"
        block_sum_functions = "\n" + text_indent(block_sum_functions, "    " * 3)  # TODO calculate indent
    else:  # not indexed
        # broadcast when a result array is provided
        # otherwise let LHS be created dynamically
        broadcast_opt = "[:]" if result_passed else ""

    # construct template
    # FUTURE consider errno or errno-like arg to retrieve extra information from namespace
    if not indexers:
        T = f"""
        def expressive_wrapper({block_args}):
            {expr.lhs}{broadcast_opt} = {expr.rhs}
            return {name_result}
        """
    elif len(indexers) == 1:
        indexer, (start, end) = next(iter(indexers.items()))
        # construct range sequence
        start = -start  # flip start to be positive (no -0 in "normal" Python)
        end   = "length" if end == 0 else f"length - {end}"
        if use_native_threadpool:
            block_length = f"length = len({name_size_symbol})"
            block_range  = "range(_offset_start, _offset_end)"
        else:
            block_length = f"length = len({name_size_symbol})"
            range_fn = "prange" if allow_prange else "range"
            # start = -start  # flip start to be positive (no -0 in "normal" Python)
            # end   = f"length" if end == 0 else f"length - {end}"
            block_range  = f"{range_fn}({start}, {end})"

        # FIXME improve accounting for result LHS in range
        #   consider disallowing negative LHS offset, though it could be useful
        T = f"""
        def expressive_wrapper({block_args}):
            {block_sum_functions}
            {block_length}
            {block_result}
            for {indexer} in {block_range}:
                {expr.lhs} = {expr.rhs}
            return {name_result}
        """
    else:
        # FUTURE consider if it's possible to implement this as nested loops [ISSUE 91]
        raise RuntimeError(f"BUG: indexers must be len 1 when provided (see string_expr_to_sympy): {indexers}")

    # tidy up template
    T = text_dedent(T)

    # build and extract
    exec(T, expr_namespace)
    fn = expr_namespace["expressive_wrapper"]

    return fn
