#   License: BSD-3-Clause
#   Author: LKouadio <etanoyau@gmail.com>

import warnings 
from typing import Any, Optional, List, Union
import numpy as np 
import pandas as pd 

from ..core.array_manager import drop_nan_in, array_preserver, to_array 
from ..core.checks import check_empty, ensure_same_shape
from ..core.io import is_data_readable, SaveFile  
from ..core.utils import error_policy 

from ..decorators import Dataify 
from ..utils.base_utils import fill_NaN 

@SaveFile
@is_data_readable 
@check_empty(['data', 'auxi_data']) 
def nan_ops(
    data,
    auxi_data = None,
    data_kind = None,
    ops = 'check_only',
    action = None,
    error = 'raise',
    process = None,
    condition = None,
    savefile=None,
    verbose = 0,
):
    r"""
    Perform operations on NaN values within data structures, handling both
    primary data and optional witness data based on specified parameters.

    This function provides a comprehensive toolkit for managing missing
    values (`NaN`) in various data structures such as NumPy arrays,
    pandas DataFrames, and pandas Series. Depending on the `ops` parameter,
    it can check for the presence of `NaN`s, validate data integrity, or
    sanitize the data by filling or dropping `NaN` values. The function
    also supports handling witness data, which can be crucial in scenarios
    where the relationship between primary and witness data must be maintained.

    .. math::
       \text{Processed\_data} =
       \begin{cases}
           \text{filled\_data} & \text{if action is 'fill'} \\
           \text{dropped\_data} & \text{if action is 'drop'} \\
           \text{original\_data} & \text{otherwise}
       \end{cases}

    Parameters
    ----------
    data : array-like, pandas.DataFrame, or pandas.Series
        The primary data structure containing `NaN` values to be processed.
        
    auxi_data : array-like, pandas.DataFrame, or pandas.Series, optional
        Auxiliary data that accompanies the primary `data`. Its role depends
        on the ``data_kind`` parameter. If ``data_kind`` is `'target'`,
        ``auxi_data`` is treated as feature data, and vice versa. This is
        useful for operations that need to maintain the alignment between
        primary and witness data.
        
    data_kind : {'target', 'feature', None}, optional
        Specifies the role of the primary `data`. If set to `'target'`, `data`
        is considered target data, and ``auxi_data`` (if provided) is
        treated as feature data. If set to `'feature'`, `data` is treated as
        feature data, and ``auxi_data`` is considered target data. If
        `None`, no special handling is applied, and witness data is ignored
        unless explicitly required by other parameters.
        
    ops : {'check_only', 'validate', 'sanitize'}, default ``'check_only'``
        Defines the operation to perform on the `NaN` values in the data:

        - ``'check_only'``: Checks whether the data contains any `NaN` values
          and returns a boolean indicator.
        - ``'validate'``: Validates that the data does not contain `NaN` values.
          If `NaN`s are found, it raises an error or warns based on the
          ``error`` parameter.
        - ``'sanitize'``: Cleans the data by either filling or dropping `NaN`
          values based on the ``action``, ``process``, and ``condition``
          parameters.

    action : {'fill', 'drop'}, optional
        Specifies the action to take when ``ops`` is set to `'sanitize'`:

        - ``'fill'``: Fills `NaN` values using the `fill_NaN` function with the
          method set to `'both'`.
        - ``'drop'``: Drops `NaN` values based on the conditions and process
          specified. If `data_kind` is `'target'`, it handles `NaN`s in a way
          that preserves data integrity for machine learning models.
        - If `None`, defaults to `'drop'` when sanitizing.

        **Note:** If ``ops`` is not `'sanitize'` and ``action`` is set, an error
        is raised indicating conflicting parameters.

    error : {'raise', 'warn', None}, default ``'raise'``
        Determines the error handling policy:

        - ``'raise'``: Raises exceptions when encountering issues.
        - ``'warn'``: Emits warnings instead of raising exceptions.
        - ``None``: Defaults to the base policy, which is typically `'warn'`.

        This parameter is utilized by the `error_policy` function to enforce
        consistent error handling throughout the operation.

    process : {'do', 'do_anyway'}, optional
        Works in conjunction with the ``action`` parameter when ``action`` is
        `'drop'`:

        - ``'do'``: Drops `NaN` values only if certain conditions are met.
        - ``'do_anyway'``: Forces the dropping of `NaN` values regardless of
          conditions.

        This provides flexibility in handling `NaN`s based on the specific
        requirements of the dataset and the analysis being performed.

    condition : callable or None, optional
        A callable that defines a condition for dropping `NaN` values when
        ``action`` is `'drop'`. For example, it can specify that the number
        of `NaN`s should not exceed a certain fraction of the dataset. If the
        condition is not met, the behavior is controlled by the ``process``
        parameter.

    verbose : int, default ``0``
        Controls the verbosity level of the function's output for debugging
        purposes:

        - ``0``: No output.
        - ``1``: Basic informational messages.
        - ``2``: Detailed processing messages.
        - ``3``: Debug-level messages with complete trace of operations.

        Higher verbosity levels provide more insights into the function's
        internal operations, aiding in debugging and monitoring.

    Returns
    -------
    array-like, pandas.DataFrame, or pandas.Series
        The sanitized data structure with `NaN` values handled according to
        the specified parameters. If ``auxi_data`` is provided and
        processed, a tuple containing the sanitized `data` and
        `auxi_data` is returned. Otherwise, only the sanitized `data`
        is returned.

    Raises
    ------
    ValueError
        - If an invalid value is provided for ``ops`` or ``data_kind``.
        - If ``auxi_data`` does not align with ``data`` in shape.
        - If sanitization conditions are not met and the error policy is
          set to `'raise'`.
    Warning
        - Emits warnings when `NaN` values are present and the error policy is
          set to `'warn'`.

    Examples
    --------
    >>> from fusionlab.utils.data_utils import nan_ops
    >>> import pandas as pd
    >>> import numpy as np
    >>> # Example with target data and witness feature data
    >>> target = pd.Series([1, 2, np.nan, 4])
    >>> features = pd.DataFrame({
    ...     'A': [5, np.nan, 7, 8],
    ...     'B': ['x', 'y', 'z', np.nan]
    ... })
    >>> # Check for NaNs
    >>> nan_ops(target, auxi_data=features, data_kind='target', ops='check_only')
    (True, True)
    >>> # Validate data (will raise ValueError if NaNs are present)
    >>> nan_ops(target, auxi_data=features, data_kind='target', ops='validate')
    Traceback (most recent call last):
        ...
    ValueError: Target contains NaN values.
    >>> # Sanitize data by dropping NaNs
    >>> cleaned_target, cleaned_features = nan_ops(
    ...     target,
    ...     auxi_data=features,
    ...     data_kind='target',
    ...     ops='sanitize',
    ...     action='drop',
    ...     verbose=2
    ... )
    Dropping NaN values.
    Dropped NaNs successfully.
    >>> cleaned_target
    0    1.0
    1    2.0
    3    4.0
    dtype: float64
    >>> cleaned_features
         A    B
    0  5.0    x
    3  8.0  NaN

    Notes
    -----
    The `nan_ops` function is designed to provide a robust framework for handling
    missing values in datasets, especially in machine learning workflows where
    the integrity of target and feature data is paramount. By allowing
    conditional operations and providing flexibility in error handling, it ensures
    that data preprocessing can be tailored to the specific needs of the analysis.

    The function leverages helper utilities such as `fill_NaN`, `drop_nan_in`,
    and `error_policy` to maintain consistency and reliability across different
    data structures and scenarios. The verbosity levels aid developers in tracing
    the function's execution flow, making it easier to debug and verify data
    transformations.

    See Also
    --------
    gofast.utils.base_utils.fill_NaN` :
        Fills `NaN` values in numeric data structures using specified methods.
    gofast.core.array_manager.drop_nan_in:
        Drops `NaN` values from data structures, optionally alongside witness data.
    gofast.core.utils.error_policy:
        Determines how errors are handled based on user-specified policies.
    gofast.core.array_manager.array_preserver:
        Preserves and restores the original structure of array-like data.

    """

    # Helper function to check for NaN values in the data.
    def has_nan(d):
        if isinstance(d, pd.DataFrame):
            return d.isnull().any().any()
        return pd.isnull(d).any()
    
    # Helper function to return data and auxi_data based on availability.
    def return_kind(dval, wval=None):
        if auxi_data is not None:
            return dval, wval
        return dval
    
    # Helper function to drop NaNs from data and auxi_data.
    def drop_nan(d, wval=None):
        if auxi_data is not None:
            d_cleaned, w_cleaned = drop_nan_in(d, wval, axis=0)
        else:
            d_cleaned = drop_nan_in(d, solo_return=True, axis=0)
            w_cleaned = None
        return d_cleaned, w_cleaned
    
    # Helper function to log messages based on verbosity level.
    def log(message, level):
        if verbose >= level:
            print(message)
    
    # Apply the error policy to determine how to handle errors.
    error = error_policy(
        error, base='warn', valid_policies={'raise', 'warn'}
    )
    
    # Validate that 'ops' parameter is one of the allowed operations.
    valid_ops = {'check_only', 'validate', 'sanitize'}
    if ops not in valid_ops:
        raise ValueError(
            f"Invalid ops '{ops}'. Choose from {valid_ops}."
        )
    
    # Ensure 'data_kind' is either 'target', 'feature', or None.
    if data_kind not in {'target', 'feature', None}:
        raise ValueError(
            "Invalid data_kind. Choose from 'target', 'feature', or None."
        )
    
    # If 'auxi_data' is provided, ensure it matches the shape of 'data'.
    if auxi_data is not None:
        try:
            ensure_same_shape(data, auxi_data, axis=None)
            log("Auxiliary data shape matches data.", 3)
        except Exception as e:
            raise ValueError(
                f"Auxiliary data shape mismatch: {e}"
            )
    
    # Determine if 'data' and 'auxi_data' contain NaN values.
    data_contains_nan = has_nan(data)
    w_contains_nan = has_nan(auxi_data) if auxi_data is not None else False
    
    # Define subjects based on 'data_kind' for clearer messaging.
    subject = 'Data' if data_kind is None else data_kind.capitalize()
    w_subject = "Auxiliary data" if data_kind is None else (
        "Feature" if subject == 'Target' else 'Target'
    )
    
    # Handle 'check_only' operation: simply return NaN presence status.
    if ops == 'check_only':
        log("Performing NaN check only.", 1)
        return return_kind(data_contains_nan, w_contains_nan)
    
    # Handle 'validate' operation: raise errors or warnings if NaNs are present.
    if ops == 'validate':
        log("Validating data for NaN values.", 1)
        if data_contains_nan:
            message = f"{subject} contains NaN values."
            if error == 'raise':
                raise ValueError(message)
            elif error == 'warn':
                warnings.warn(message)
        if w_contains_nan:
            message = f"{w_subject} contains NaN values."
            if error == 'raise':
                raise ValueError(message)
            elif error == 'warn':
                warnings.warn(message)
        log("Validation complete. No NaNs detected or handled.", 2)
        return return_kind(data, auxi_data)
    
    # For 'sanitize' operation, proceed to handle NaN values based on 'action'.
    if ops == 'sanitize':
        log("Sanitizing data by handling NaN values.", 1)
        # Preserve the original structure of the data.
        collected = array_preserver(data, auxi_data, action='collect')
        
        # Convert inputs to array-like structures for processing.
        data_converted = to_array(data)
        auxi_converted = to_array(auxi_data) if auxi_data is not None else None
        
        # If 'action' is not specified, default to 'drop'.
        if action is None:
            action = 'drop'
            log("No action specified. Defaulting to 'drop'.", 2)
        
        # Handle 'fill' action: fill NaNs using the 'fillNaN' function.
        if action == 'fill':
            log("Filling NaN values.", 2)
            data_filled = fill_NaN(data_converted, method='both')
            if auxi_data is not None:
                auxi_filled = fill_NaN(auxi_converted, method='both')
            else:
                auxi_filled = None
            log("NaN values filled successfully.", 3)
            return return_kind(data_filled, auxi_filled)
        
        # Handle 'drop' action: drop NaNs based on 'data_kind' and 'process'.
        elif action == 'drop':
            log("Dropping NaN values.", 2)
            nan_count = (
                data_converted.isnull().sum().sum()
                if isinstance(data_converted, pd.DataFrame)
                else pd.isnull(data_converted).sum()
            )
            data_length = len(data_converted)
            log(f"NaN count: {nan_count}, Data length: {data_length}", 3)
            
            # Specific handling when 'data_kind' is 'target'.
            if data_kind == 'target':
                # Define condition: NaN count should be less than half of data length.
                if condition is None:
                    condition = (nan_count < (data_length / 2))
                    log(
                        "No condition provided. Setting condition to "
                        f"NaN count < {data_length / 2}.",
                        3
                    )
                
                # If condition is not met, decide based on 'process'.
                if not condition:
                    if process == 'do_anyway':
                        log(
                            "Condition not met. Proceeding to drop NaNs "
                            "anyway.", 2
                        )
                        data_cleaned, auxi_cleaned = drop_nan(data, auxi_data)
                    else:
                        warning_msg = (
                            "NaN values in target exceed half the data length. "
                            "Dropping these NaNs may lead to significant information loss."
                        )
                        error_msg = (
                            "Too many NaN values in target data. "
                            "Consider revisiting the target variable."
                        )
                        if error == 'warn':
                            warnings.warn(warning_msg)
                        raise ValueError(error_msg)
                else:
                    # Condition met: proceed to drop NaNs.
                    log("Condition met. Dropping NaNs.", 3)
                    data_cleaned, auxi_cleaned = drop_nan(data, auxi_data)
            
            # Handling when 'data_kind' is 'feature' or None.
            elif data_kind in {'feature', None}:
                if process == 'do_anyway':
                    log(
                        "Process set to 'do_anyway'. Dropping NaNs regardless "
                        "of conditions.", 2
                    )
                    condition = None  # Reset condition to drop unconditionally
                
                if condition is None:
                    log("Dropping NaNs unconditionally.", 3)
                    data_cleaned, auxi_cleaned = drop_nan(data, auxi_data)
                else:
                    # Example condition: NaN count should be less than a third of data length.
                    condition_met = (nan_count < condition)
                    log(
                        f"Applying condition: NaN count < {data_length / 3} -> "
                        f"{condition_met}", 3
                    )
                    if not condition_met:
                        if process == 'do_anyway':
                            log(
                                "Condition not met. Dropping NaNs anyway.", 2
                            )
                            data_cleaned, auxi_cleaned = drop_nan(data, auxi_data)
                        else:
                            warning_msg = (
                                "NaN values exceed the acceptable limit based on "
                                "the condition. Dropping may remove significant data."
                            )
                            error_msg = (
                                "Condition for dropping NaNs not met. "
                                "Consider adjusting the condition or processing parameters."
                            )
                            if error == 'warn':
                                warnings.warn(warning_msg)
                            raise ValueError(error_msg)
                    else:
                        # Condition met: proceed to drop NaNs.
                        log("Condition met. Dropping NaNs.", 3)
                        data_cleaned, auxi_cleaned = drop_nan(data, auxi_data)
            
            # Assign cleaned data back to variables.
            data_filled = data_cleaned
            auxi_filled = auxi_cleaned if auxi_data is not None else None
            
            # Handle verbose messages for the cleaned data.
            if verbose >= 2:
                log("NaN values have been dropped from the data.", 2)
                if auxi_filled is not None:
                    log("NaN values have been dropped from the witness data.", 2)
            
        else:
            # If 'action' is not recognized, raise an error.
            raise ValueError(
                f"Invalid action '{action}'. Choose from 'fill', 'drop', or None."
            )
        
        # Restore the original array structure using the preserved properties.
        collected['processed'] = [data_filled, auxi_filled]
        try:
            
            data_restored, auxi_restored = array_preserver(
                collected, action='restore'
            )
            log("Data structure restored successfully.", 3)
        except Exception as e:
            log(
                f"Failed to restore data structure: {e}. Returning filled data as is.",
                1
            )
            data_restored = data_filled
            auxi_restored = auxi_filled
        
        # Return the cleaned data and auxi_data if available.
        
        return return_kind(data_restored, auxi_restored)
@SaveFile  
@is_data_readable 
@Dataify(auto_columns=True, fail_silently=True) 
def mask_by_reference(
    data: pd.DataFrame,
    ref_col: str,
    values: Optional[Union[Any, List[Any]]] = None,
    find_closest: bool = False,
    fill_value: Any = 0,
    mask_columns: Optional[Union[str, List[str]]] = None,
    error: str = "raise",
    verbose: int = 0,
    inplace: bool = False,
    savefile:Optional[str]=None, 
) -> pd.DataFrame:
    r"""
    Masks (replaces) values in columns other than the reference column
    for rows in which the reference column matches (or is closest to) the
    specified value(s).

    If a row's reference-column value is matched, that row's values in
    the *other* columns are overwritten by ``fill_value``. The reference
    column itself is not modified.

    This function supports both exact and approximate matching:
      - **Exact** matching is used if ``find_closest=False``.
      - **Approximate** (closest) matching is used if
        ``find_closest=True`` and the reference column is numeric.

    By default, if the reference column does not exist or if the
    given ``values`` cannot be found (or approximated) in the reference
    column, an exception is raised. This behavior can be adjusted with
    the ``error`` parameter.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame containing the data to be masked.

    ref_col : str
        The column in ``data`` serving as the reference for matching
        or finding the closest values.

    values : Any or sequence of Any, optional
        The reference values to look for in ``ref_col``. This can be:
          - A single value (e.g., ``0`` or ``"apple"``).
          - A list/tuple of values (e.g., ``[0, 10, 25]``).
          - If ``values`` is None, **all rows** are masked 
            (i.e. all rows match), effectively overwriting the entire
            DataFrame (except the reference column) with ``fill_value``.
        
        Note that if ``find_closest=False``, these values must appear
        in the reference column; otherwise, an error or warning is
        triggered (depending on the ``error`` setting).

    find_closest : bool, default=False
        If True, performs an approximate match for numeric reference
        columns. For each entry in ``values``, the function locates
        the row(s) in ``ref_col`` whose value is numerically closest.
        Non-numeric reference columns will revert to exact matching
        regardless.

    fill_value : Any, default=0
        The value used to fill/mask the non-reference columns wherever
        the condition (exact or approximate match) is met. This can
        be any valid type, e.g., integer, float, string, np.nan, etc.
        If ``fill_value='auto'`` and multiple values
        are given, each row matched by a particular reference
        value is filled with **that same reference value**.

        **Examples**:
          - If ``values=9`` and ``fill_value='auto'``, the fill
            value is **9** for matched rows.
          - If ``values=['a', 10]`` and ``fill_value='auto'``,
            then rows matching `'a'` are filled with `'a'`, and
            rows matching `10` are filled with `10`.
            
    mask_columns : str or list of str, optional
        If specified, *only* these columns are masked. If None,
        all columns except ``ref_col`` are masked. If any column in
        ``mask_columns`` does not exist in the DataFrame and
        ``error='raise'``, a KeyError is raised; otherwise, a warning
        may be issued or ignored.

    error : {'raise', 'warn', 'ignore'}, default='raise'
        Controls how to handle errors:
          - 'raise': raise an error if the reference column does not
            exist or if any of the given values cannot be matched (or
            approximated).
          - 'warn': only issue a warning instead of raising an error.
          - 'ignore': silently ignore any issues.

    verbose : int, default=0
        Verbosity level:
          - 0: silent (no messages).
          - 1: minimal feedback.
          - 2 or 3: more detailed messages for debugging.

    inplace : bool, default=False
        If True, performs the operation in place and returns the 
        original DataFrame with modifications. If False, returns a
        modified copy, leaving the original unaltered.
        
    savefile : str or None, optional
        File path where the DataFrame is saved if the
        decorator-based saving is active. If `None`, no saving
        occurs.

    Returns
    -------
    pd.DataFrame
        A DataFrame where rows matching the specified condition (exact
        or approximate) have had their non-reference columns replaced by
        ``fill_value``.

    Raises
    ------
    KeyError
        If ``error='raise'`` and ``ref_col`` is not in ``data.columns``.
    ValueError
        If ``error='raise'`` and no exact/approx match can be found
        for one or more entries in ``values``.

    Notes
    -----
    - If ``values`` is None, **all** rows are masked in the non-ref
      columns, effectively overwriting them with ``fill_value``.
    - When ``find_closest=True``, approximate matching is performed only
      if the reference column is numeric. For non-numeric data, it falls
      back to exact matching.
    - When multiple reference values are provided, each is
      processed in turn. If `fill_value='auto'`, each matched row
      is filled with that specific reference value.

    Examples
    --------
    >>> import pandas as pd
    >>> from fusionlab.utils.data_utils import mask_by_reference
    >>>
    >>> df = pd.DataFrame({
    ...     "A": [10, 0, 8, 0],
    ...     "B": [2, 0.5, 18, 85],
    ...     "C": [34, 0.8, 12, 4.5],
    ...     "D": [0, 78, 25, 3.2]
    ... })
    >>>
    >>> # Example 1: Exact matching, replace all columns except 'A' with 0
    >>> masked_df = mask_by_reference(
    ...     data=df,
    ...     ref_col="A",
    ...     values=0,
    ...     fill_value=0,
    ...     find_closest=False,
    ...     error="raise"
    ... )
    >>> print(masked_df)
    >>> # 'B', 'C', 'D' for rows where A=0 are replaced with 0.
    >>>
    >>> # Example 2: Approximate matching for numeric
    >>> # If 'A' has values [0, 10, 8] and we search for 9, then 'A=8' or 'A=10'
    >>> # are the closest, so those rows get masked in non-ref columns.
    >>> masked_df2 = mask_by_reference(
    ...     data=df,
    ...     ref_col="A",
    ...     values=9,
    ...     find_closest=True,
    ...     fill_value=-999
    ... )
    >>> print(masked_df2)
    
    >>>
    >>> # Example 2: Approx. match for numeric ref_col
    >>> # 9 is between 8 and 10, so rows with A=8 and A=10 are masked
    >>> res2 = mask_by_reference(df, "A", 9, find_closest=True, fill_value=-999)
    >>> print(res2)
    ... # Rows 0 (A=10) and 2 (A=8) are replaced with -999 in columns B,C,D
    >>>
    >>> # Example 3: fill_value='auto' with multiple values
    >>> # Rows matching A=0 => fill with 0; rows matching A=8 => fill with 8
    >>> res3 = mask_by_reference(df, "A", [0, 8], fill_value='auto')
    >>> print(res3)
    ... # => rows with A=0 => B,C,D replaced by 0
    ... # => rows with A=8 => B,C,D replaced by 8
    >>> 
    >>> # 2) mask_columns=['C','D'] => only columns C and D are masked
    >>> res2 = mask_by_reference(df, "A", values=0, fill_value=999,
    ...                         mask_columns=["C","D"])
    >>> print(res2)
    ... # Rows where A=0 => columns C,D replaced by 999, while B remains unchanged
    >>>
    """
    # --- Preliminary checks --- #
    if ref_col not in data.columns:
        msg = (f"[mask_by_reference] Column '{ref_col}' not found "
               f"in the DataFrame.")
        if error == "raise":
            raise KeyError(msg)
        elif error == "warn":
            warnings.warn(msg)
            return data  # return as is
        else:
            return data  # error=='ignore'

    # Decide whether to operate on a copy or in place
    df = data if inplace else data.copy()

    # Determine which columns we'll mask
    if mask_columns is None:
        # mask all except ref_col
        mask_cols = [c for c in df.columns if c != ref_col]
    else:
        # Convert a single string to list
        if isinstance(mask_columns, str):
            mask_columns = [mask_columns]

        # Check that columns exist
        not_found = [col for col in mask_columns if col not in df.columns]
        if len(not_found) > 0:
            msg_cols = (f"[mask_by_reference] The following columns were "
                        f"not found in DataFrame: {not_found}.")
            if error == "raise":
                raise KeyError(msg_cols)
            elif error == "warn":
                warnings.warn(msg_cols)
                # Remove them from mask list if ignoring/warning
                mask_columns = [c for c in mask_columns if c in df.columns]
            else:
                pass  # silently ignore
        mask_cols = [c for c in mask_columns if c != ref_col]

    if verbose > 1:
        print(f"[mask_by_reference] Columns to be masked: {mask_cols}")

    # If values is None => mask all rows in mask_cols
    if values is None:
        if verbose > 0:
            print("[mask_by_reference] 'values' is None. Masking ALL rows.")
        if fill_value == 'auto':
            # 'auto' doesn't make sense with None => fill with None
            if verbose > 0:
                print("[mask_by_reference] 'fill_value=auto' but no values "
                      "specified. Will use None for fill.")
            df[mask_cols] = None
        else:
            df[mask_cols] = fill_value
        return df

    # Convert single value to a list
    if not isinstance(values, (list, tuple, set)):
        values = [values]

    ref_series = df[ref_col]
    is_numeric = pd.api.types.is_numeric_dtype(ref_series)

    # If find_closest and ref_series isn't numeric => revert to exact
    if find_closest and not is_numeric:
        if verbose > 0:
            print("[mask_by_reference] 'find_closest=True' but reference "
                  "column is not numeric. Reverting to exact matching.")
        find_closest = False

    total_matched_rows = set()  # track distinct row indices matched

    # Loop over each value and find matched rows
    for val in values:
        if find_closest:
            # Approximate match for numeric
            distances = (ref_series - val).abs()
            min_dist = distances.min()
            # If min_dist is inf, no numeric interpretation possible
            if min_dist == np.inf:
                matched_idx = []
            else:
                matched_idx = distances[distances == min_dist].index
        else:
            # Exact match
            matched_idx = ref_series[ref_series == val].index

        if len(matched_idx) == 0:
            # No match found for val
            msg_val = (
                f"[mask_by_reference] No matching value found for '{val}'"
                f" in column '{ref_col}'. Ensure '{val}' exists in "
                f"'{ref_col}' before applying the mask, or set"
                " ``find_closest=True`` to select the closest match."
            )
            if find_closest:
                msg_val = (f"[mask_by_reference] Could not approximate '{val}' "
                           f"in numeric column '{ref_col}'.")
            if error == "raise":
                raise ValueError(msg_val)
            elif error == "warn":
                warnings.warn(msg_val)
                continue  # skip
            else:
                continue  # error=='ignore'
        else:
            # Decide the actual fill we use for these matches
            if fill_value == 'auto':
                fill = val
            else:
                fill = fill_value

            # Mask these matched rows
            df.loc[matched_idx, mask_cols] = fill

            # Accumulate matched indices
            total_matched_rows.update(matched_idx)

    if verbose > 0:
        distinct_count = len(total_matched_rows)
        print(f"[mask_by_reference] Distinct matched rows: {distinct_count}")

    return df