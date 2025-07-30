from iode.iode_cython import cython_load_extra_files as cython_load_extra_files, cython_reset_extra_files as cython_reset_extra_files
from iode.util import enable_msgs as enable_msgs, suppress_msgs as suppress_msgs
from pathlib import Path

def load_extra_files(extra_files: str | Path | list[str | Path], quiet: bool = False) -> list[Path]:
    '''
    Load extra file(s) referenced in generalized samples.
    Maximum 4 files can be passed as argument.
    The file [1] always refers to the current workspace. 
    Extra files are numerated from 2 to 5.

    Parameters
    ----------
    extra_files: str or Path or list(str) or list(Path)
        The extra files to load. Can be a single file, a list of files, 
        or a string with file paths separated by semicolons.
    quiet: bool, optional
        If True, suppresses the log messages during the loading of files. 
        Default is False.
            
    Examples
    --------
    >>> from pathlib import Path
    >>> from iode import SAMPLE_DATA_DIR
    >>> from iode import load_extra_files

    >>> sample_data_dir = Path(SAMPLE_DATA_DIR)
    >>> extra_files = [sample_data_dir / "ref.av", sample_data_dir / "fun.av", 
    ...                sample_data_dir / "fun2.av", sample_data_dir / "a.var"]
    >>> extra_files = load_extra_files(extra_files)         # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Loading ...\\ref.av
    ...
    394 objects loaded
    Loading ...\\fun.av
    ...
    394 objects loaded
    Loading ...\\fun2.av
    ...
    394 objects loaded
    Loading ...\\a.var
    433 objects loaded
    >>> extra_files = load_extra_files(extra_files, quiet=True)
    >>> [Path(filepath).name for filepath in extra_files]
    [\'ref.av\', \'fun.av\', \'fun2.av\', \'a.var\']
    '''
def reset_extra_files() -> None:
    '''
    reset extra files referenced in generalized samples.

    Parameters
    ----------
    extra_files: str or Path or list(str) or list(Path)

    Examples
    --------
    >>> from pathlib import Path
    >>> from iode import SAMPLE_DATA_DIR
    >>> from iode import load_extra_files, reset_extra_files

    >>> sample_data_dir = Path(SAMPLE_DATA_DIR)
    >>> extra_files = [sample_data_dir / "ref.av", sample_data_dir / "fun.av", 
    ...                sample_data_dir / "fun2.av", sample_data_dir / "a.var"]
    >>> extra_files = load_extra_files(extra_files, quiet=True)
    >>> [Path(filepath).name for filepath in extra_files]
    [\'ref.av\', \'fun.av\', \'fun2.av\', \'a.var\']

    >>> reset_extra_files()
    >>> load_extra_files([])
    []
    '''
