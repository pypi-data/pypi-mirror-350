# -*- coding: utf-8 -*-
# Author: LKouadio <etanoyau@gmail.com>
# License: Apache License 2.0 (see LICENSE file)
# -------------------------------------------------------------------
# Provides base I/O functions for dataset management (cache dir, download).
# Adapted or inspired by the 'gofast.datasets.io' module from the
# 'gofast' package: https://github.com/earthai-tech/gofast
# Original 'gofast' code licensed under BSD-3-Clause.
# Modifications and 'fusionlab' are under Apache License 2.0.
# -------------------------------------------------------------------
"""
Internal Dataset Storage and Retrieval Utilities
(:mod:`fusionlab.datasets._property`)
=================================================

This internal module provides base functions for managing the local
storage location (cache directory) for datasets used or downloaded by
`fusionlab`. It includes utilities to determine the data directory
path, remove cached data, and potentially download remote dataset
files based on predefined metadata.

These functions are typically intended for internal use by dataset
loading functions within the :mod:`fusionlab.datasets` subpackage and
are not guaranteed to have a stable API for end-users.
"""

from __future__ import annotations 

import os
import shutil
import warnings
from importlib import resources # Used in download_file_if # noqa 
from collections import namedtuple
from typing import Optional, Union
from urllib.parse import urljoin

try:
    from ..utils.base_utils import check_file_exists, fancier_downloader 
except ImportError:
    warnings.warn("Could not import IO utilities from fusionlab.utils.io")
    # Define dummy functions if needed for
    # static analysis, but runtime will fail
    def check_file_exists(*args, **kwargs): return False
    def fancier_downloader(*args, **kwargs): raise NotImplementedError


FLAB_DMODULE = "fusionlab.datasets.data" 
KD_DESCR = "fusionlab.datasets.descr" 
FLAB_REMOTE_DATA_URL = ( 
    'https://raw.githubusercontent.com/earthai-tech/fusionlab/main/'
    'fusionlab/datasets/data/'
)

RemoteMetadata = namedtuple(
    "RemoteMetadata",
    ["file", "url", "checksum", "descr_module", "data_module"]
)


__all__ = [
    'FLAB_DMODULE', 
    'FLAB_REMOTE_DATA_URL', 
    'get_data', 
    'remove_data',
    
]


def get_data(data_home: Optional[str] = None) -> str:
    """Get the path to the fusionlab data cache directory.

    Determines the local directory path used for caching downloaded
    datasets or storing user-provided data relevant to fusionlab.
    The directory is created if it doesn't exist.

    The location defaults to ``~/fusionlab_data`` but can be overridden
    by setting the ``FUSIONLAB_DATA`` environment variable or by
    providing an explicit path to the `data_home` argument.

    Parameters
    ----------
    data_home : str, optional
        Explicit path to the desired data directory. If ``None``,
        checks the 'FUSIONLAB_DATA' environment variable, then falls
        back to ``~/fusionlab_data``. Tilde ('~') is expanded to the
        user's home directory. Default is ``None``.

    Returns
    -------
    data_dir : str
        The absolute path to the fusionlab data cache directory.

    Examples
    --------
    >>> from fusionlab.datasets._property import get_data # Use actual import
    >>> default_path = get_data()
    >>> print(f"Default data directory: {default_path}")
    >>> custom_path = get_data("/path/to/my/kdata")
    >>> print(f"Custom data directory: {custom_path}")
    """
    if data_home is None:
        # Check environment variable first
        data_home = os.environ.get(
            "FUSIONLAB_DATA", os.path.join("~", "fusionlab_data")
        )
    # Expand user path (~ character)
    data_home = os.path.expanduser(data_home)
    # Create directory if it doesn't exist
    try:
        os.makedirs(data_home, exist_ok=True)
    except OSError as e:
        # Handle potential permission errors, etc.
        warnings.warn(f"Could not create data directory {data_home}: {e}")
        # Optionally raise or return a default path if creation fails
    return data_home

def remove_data(data_home: Optional[str] = None) -> None:
    """Delete the fusionlab data cache directory and its contents.

    Removes the entire directory specified by `data_home` (or the
    default fusionlab cache directory if `data_home` is ``None``).
    Use with caution, as this permanently deletes cached data.

    Parameters
    ----------
    data_home : str, optional
        The path to the fusionlab data directory to remove. If ``None``,
        locates the directory using :func:`get_data`.
        Default is ``None``.

    Returns
    -------
    None

    Examples
    --------
    >>> from fusionlab.datasets._property import remove_data, get_data
    >>> # To remove the default cache:
    >>> # remove_data()
    >>> # To remove a custom cache:
    >>> # custom_path = get_data("/path/to/my/kdata")
    >>> # remove_data(custom_path)
    """
    # Get the path to the data directory
    data_dir = get_data(data_home)
    # Remove the directory tree if it exists
    if os.path.exists(data_dir):
        print(f"Removing fusionlab data cache directory: {data_dir}")
        shutil.rmtree(data_dir)
    else:
        print(f"fusionlab data cache directory not found: {data_dir}")

 
def download_file_if_missing(
    metadata: RemoteMetadata | str,
    data_home: Optional[str] = None,
    download_if_missing: bool = True,
    error: str = 'raise',
    verbose: bool = True
) -> Optional[str]:
    """Download and cache a remote file if not present locally.

    Checks if a file defined by `metadata` exists in the local
    fusionlab data cache directory (determined by `get_data`). If
    the file is missing and `download_if_missing` is True, it
    attempts to download it from the specified URL.

    Parameters
    ----------
    metadata : RemoteMetadata or str
        Metadata defining the remote file. Must contain at least
        `file` (filename) and `url` (base URL) attributes if a
        `RemoteMetadata` object. If a string is provided, it's
        treated as the filename, and the default module URL
        (`FLAB_REMOTE_DATA_URL`) is used.

    data_home : str, optional
        Path to the fusionlab data cache directory. If ``None``, uses
        the default location determined by :func:`get_data`.
        Default is ``None``.

    download_if_missing : bool, default=True
        If ``True``, attempt to download the file if it's not found
        in the local cache. If ``False``, only checks existence and
        returns the path if found, otherwise returns ``None``.

    error : {'raise', 'warn', 'ignore'}, default='raise'
        Determines behavior if the download fails:
        - ``'raise'``: Raises a RuntimeError.
        - ``'warn'``: Issues a warning and returns ``None``.
        - ``'ignore'``: Silently ignores the error and returns ``None``.

    verbose : bool, default=True
        If ``True``, prints status messages about checking, downloading,
        or finding the file.

    Returns
    -------
    filepath : str or None
        The absolute path to the local file if it exists or was
        successfully downloaded. Returns ``None`` if the file is missing
        and `download_if_missing` is ``False``, or if the download
        fails and `error` is not 'raise'.

    Raises
    ------
    ValueError
        If the `error` parameter is invalid.
    RuntimeError
        If the download fails and `error` is set to `'raise'`.
    TypeError
        If `metadata` is not a string or `RemoteMetadata` instance.
    """
    # Validate error parameter
    if error not in ['warn', 'raise', 'ignore']:
        raise ValueError(
            "`error` parameter must be 'raise', 'warn', or 'ignore'."
        )

    # Handle string input for metadata convenience
    if isinstance(metadata, str):
        # Assume string is filename, use default URL
        if not FLAB_REMOTE_DATA_URL:
             msg = ("Default remote data URL is not configured. Cannot "
                    "download file specified only by name.")
             if error == 'raise': raise ValueError(msg)
             elif error == 'warn': warnings.warn(msg)
             return None
        # Create a minimal metadata object
        metadata = RemoteMetadata(
            file=metadata,
            url=FLAB_REMOTE_DATA_URL,
            checksum=None, # No checksum provided
            descr_module=None,
            data_module=FLAB_DMODULE
        )
    elif not isinstance(metadata, RemoteMetadata):
        raise TypeError(
            "`metadata` must be a string (filename) or RemoteMetadata."
        )
    

    # Determine target cache directory
    data_dir = get_data(data_home)
    # Construct the full local path for the file
    local_filepath = os.path.join(data_dir, metadata.file)
    # Check if file exists locally
    file_exists = os.path.exists(local_filepath)
    
    if not file_exists: 
        # Construct the full path to the file within the package using importlib.resources
        package_path = str(resources.files(FLAB_DMODULE).joinpath(metadata.file))
        # Determine the directory where the file should be saved
        data_dir = os.path.dirname(package_path)
        # Ensure the destination directory exists to prevent
        # errors during download
        os.makedirs(data_dir, exist_ok=True)
        # Check if the specified file already exists within the given package
        file_exists = check_file_exists(FLAB_DMODULE, metadata.file)
    
    if file_exists:
        if verbose:
            print(f"Data file '{metadata.file}' found in cache:"
                  f" {data_dir}")
        return local_filepath
    
    elif not download_if_missing:
        if verbose:
            print(f"Data file '{metadata.file}' not found in cache and "
                  f"download is disabled.")
        return None
    else:
        # File missing and download enabled, proceed with download
        if verbose:
            print(f"Data file '{metadata.file}' not found in cache. "
                  f"Attempting download from {metadata.url}...")

        # Construct the full URL
        # Ensure base URL ends with / if not already present
        base_url = metadata.url if metadata.url.endswith('/') else metadata.url + '/'
        file_url = urljoin(base_url, metadata.file)

        try:
            # Use fancier_downloader: downloads to CWD then moves to dstpath
            # So, dstpath should be the target directory `data_dir`
            # filename should be just the basename
            fancier_downloader(
                url=file_url,
                filename=metadata.file, # Download as this name locally first
                dstpath=data_dir,       # Move it here after download
                check_size=True,        # Check size against header
                error=error,            # Propagate error handling
                verbose=verbose         # Control downloader verbosity
            )
            # If downloader didn't raise error, file should now be at local_filepath
            if os.path.exists(local_filepath):
                 if verbose >=2: # Add higher verbosity level if needed
                     print(f"Download successful: '{local_filepath}'")
                 return local_filepath
            else:
                 # This case *shouldn't* happen if fancier_downloader worked
                 # without raising an error, but handle defensively.
                 msg=f"Download reported success but file not found at {local_filepath}"
                 if error == 'raise': raise RuntimeError(msg)
                 elif error == 'warn': warnings.warn(msg)
                 return None

        except Exception as e:
            # Handle exceptions raised by fancier_downloader or os calls
            # The error handling logic might be duplicated if fancier_downloader
            # also raises/warns based on 'error', but this catches other issues.
            download_error_msg = (
                f"Failed to download or cache '{metadata.file}' from "
                f"'{file_url}'. Error: {e}"
            )
            if error == 'raise':
                raise RuntimeError(download_error_msg) from e
            elif error == 'warn':
                warnings.warn(download_error_msg)
            # If error is 'ignore' or 'warn', return None
            return None


def download_file_if(
    metadata: Union[RemoteMetadata, str], # Added Union for clarity
    data_home: Optional[str] = None,
    download_if_missing: bool = True,
    force_download: bool = False, # Added force_download
    error: str = 'raise',
    verbose: bool = True
) -> Optional[str]:
    """Find, cache, or download a dataset file.

    Checks for a dataset file in sequence:
    1. Checks the installed package resources.
    2. Checks the local fusionlab data cache directory.
    3. Optionally downloads to the cache if missing from both.

    If the file is found in the package resources but not in the cache,
    it is copied to the cache directory for faster future access.

    Parameters
    ----------
    metadata : RemoteMetadata or str
        Metadata defining the remote file, or just the filename string.
        If RemoteMetadata, must contain at least ``file`` and ``url``
        attributes. It should also contain ``data_module`` (e.g.,
        'fusionlab.datasets.data') specifying the package location
        to check for bundled data. If a string (filename) is
        provided, default URL (`FLAB_REMOTE_DATA_URL`) and data module
        (`KD_DATA_MODULE`) are used.

    data_home : str, optional
        Path to the fusionlab data cache directory. If ``None``, uses
        the default location determined by :func:`get_data`.
        Default is ``None``.

    download_if_missing : bool, default=True
        If ``True``, attempt to download the dataset to the cache if
        it's not found in package resources or the local cache.

    force_download : bool, default=False
        If ``True``, forces a download attempt to the cache,
        overwriting any existing file in the cache. Checks package
        resources first only if download fails. Default is ``False``.

    error : {'raise', 'warn', 'ignore'}, default='raise'
        Determines behavior if the download fails:
        - ``'raise'``: Raises a RuntimeError.
        - ``'warn'``: Issues a warning and returns ``None``.
        - ``'ignore'``: Silently ignores the error and returns ``None``.

    verbose : bool, default=True
        If ``True``, prints status messages about checking locations,
        copying, or downloading the file.

    Returns
    -------
    filepath : str or None
        The absolute path to the validated local file (usually in the
        cache directory). Returns ``None`` if the file cannot be found
        or obtained based on the specified parameters.

    Raises
    ------
    ValueError
        If the `error` parameter is invalid, or if essential metadata
        (filename, URL, data_module) is missing for download/lookup.
    RuntimeError
        If the download fails and `error` is set to `'raise'`.
    TypeError
        If `metadata` is not a string or `RemoteMetadata` instance.
    """
    # 1. Validate inputs and resolve metadata
    if error not in ['warn', 'raise', 'ignore']:
        raise ValueError(
            "`error` parameter must be 'raise', 'warn', or 'ignore'."
        )

    if isinstance(metadata, str):
        if not FLAB_REMOTE_DATA_URL or not FLAB_DMODULE:
             msg = ("Default remote URL or data module path not configured."
                    " Cannot process file specified only by name.")
             if error == 'raise': raise ValueError(msg)
             elif error == 'warn': warnings.warn(msg)
             return None
        # Create metadata object from string filename
        filename = metadata
        meta = RemoteMetadata(
            file=filename, url=FLAB_REMOTE_DATA_URL, checksum=None,
            descr_module=None, data_module=FLAB_DMODULE
        )
    elif isinstance(metadata, RemoteMetadata):
        meta = metadata
        filename = meta.file
        if not hasattr(meta, 'data_module') or not meta.data_module:
             raise ValueError("RemoteMetadata must include 'data_module' path.")
        if not hasattr(meta, 'url') or not meta.url:
             raise ValueError("RemoteMetadata must include 'url'.")
    else:
        raise TypeError(
            "`metadata` must be a string (filename) or RemoteMetadata."
        )

    # 2. Determine Cache Path
    data_dir = get_data(data_home) # User cache directory
    cache_filepath = os.path.join(data_dir, filename)

    # 3. Handle Forced Download
    if force_download:
        if download_if_missing:
            if verbose:
                print(f"Forcing download attempt for '{filename}' to {data_dir}...")
            dl_success = False
            try:
                # Construct full URL (ensure trailing slash on base URL)
                base_url = meta.url if meta.url.endswith('/') else meta.url + '/'
                file_url = urljoin(base_url, filename)
                # Use fancier_downloader to download/move to cache
                fancier_downloader(
                    url=file_url,
                    filename=filename, # Name to save as temporarily/finally
                    dstpath=data_dir,  # Target directory for move
                    check_size=True,   # Enable size check
                    error=error,       # Propagate error setting
                    verbose=verbose > 0 # Pass verbosity flag
                )
                # Check if file now exists in cache after download attempt
                if os.path.exists(cache_filepath):
                    dl_success = True # noqa
                    if verbose:
                        print(f"Forced download successful: '{cache_filepath}'")
                    return cache_filepath # Success!
                else:
                    # Should not happen if downloader worked & error!='raise'
                    msg = ("Download function reported success (or ignored "
                           f"error) but file '{filename}' not found in cache.")
                    if error == 'raise': raise RuntimeError(msg)
                    elif error == 'warn': warnings.warn(msg)
                    # Continue to check package resource as fallback only if download failed

            except Exception as e:
                # Handle exceptions from fancier_downloader
                dl_error_msg = (
                    f"Forced download failed for '{filename}'. Error: {e}"
                )
                if error == 'raise':
                    raise RuntimeError(dl_error_msg) from e
                elif error == 'warn':
                    warnings.warn(dl_error_msg)
                # Continue to check package resource as fallback only if download failed
        else:
            # Cannot force download if download_if_missing is False
            warnings.warn(f"Cannot force download for '{filename}', "
                          f"download_if_missing is False.")
            # Fall through to check package/cache normally

    # 4. Check Package Resources First (if download wasn't forced or failed)
    package_filepath = None
    try:
        if resources.is_resource(meta.data_module, filename):
            if verbose:
                print(f"Dataset '{filename}' found in package resource: "
                      f"{meta.data_module}")
            # Get path via context manager
            with resources.path(meta.data_module, filename) as rpath:
                package_filepath = str(rpath)
    except (ModuleNotFoundError, TypeError, Exception) as e:
        # ModuleNotFoundError if data_module path is wrong
        # TypeError if non-string arguments
        # Catch broad Exception for other potential resource issues
        if verbose:
             warnings.warn(f"Could not check package resources for "
                           f"'{meta.data_module}/{filename}': {e}")

    # If found in package, copy to cache if not already there (or if download failed)
    if package_filepath and not os.path.exists(cache_filepath):
        if verbose:
            print(f"Copying dataset from package to cache: {cache_filepath}")
        try:
            os.makedirs(data_dir, exist_ok=True) # Ensure cache dir exists
            shutil.copyfile(package_filepath, cache_filepath)
            return cache_filepath # Return cache path after copying
        except Exception as copy_err:
            warnings.warn(f"Could not copy dataset from package to cache: "
                          f"{copy_err}. Using package path directly.")
            # Fallback to returning the package path if copy fails? Risky.
            # Better to return None or raise? Let's return cache path anyway
            #  if copy fails but file exists in package
            # return package_filepath # Use with caution if cache is preferred
            return cache_filepath if os.path.exists(cache_filepath) else package_filepath

    # If file was found in package AND already exists in cache, use cache path
    if package_filepath and os.path.exists(cache_filepath):
         if verbose:
             print(f"Using cached version (also found in package): {cache_filepath}")
         return cache_filepath

    # 5. Check Cache Directory (if not found in package)
    if not package_filepath and os.path.exists(cache_filepath):
        if verbose:
            print(f"Dataset '{filename}' found in cache: {cache_filepath}")
        return cache_filepath

    # 6. Attempt Download (if not found in package or cache, and allowed)
    if download_if_missing:
        if verbose:
             print(f"Dataset '{filename}' not found in package or cache. "
                   f"Attempting download to {data_dir}...")
        try:
            # Construct full URL
            base_url = meta.url if meta.url.endswith('/') else meta.url + '/'
            file_url = urljoin(base_url, filename)
            # Download and move to cache
            fancier_downloader(
                url=file_url, filename=filename, dstpath=data_dir,
                check_size=True, error=error, verbose=verbose > 0
            )
            # Check if successful
            if os.path.exists(cache_filepath):
                 if verbose >=2 : print(f"Download successful: '{cache_filepath}'")
                 return cache_filepath
            else: # Download failed silently (error='ignore' or 'warn')
                 return None # Return None as download wasn't successful
        except Exception as e:
             download_error_msg = (
                f"Failed to download '{filename}' from "
                f"'{file_url}'. Error: {e}"
             )
             if error == 'raise':
                 raise RuntimeError(download_error_msg) from e
             elif error == 'warn':
                 warnings.warn(download_error_msg)
             return None # Download failed

    # 7. File Not Found and Download Disabled/Failed
    if verbose:
        print(f"Dataset '{filename}' could not be located.")
    return None