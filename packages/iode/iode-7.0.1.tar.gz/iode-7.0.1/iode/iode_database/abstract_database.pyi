from _typeshed import Incomplete
from iode.common import IODE_FILE_TYPES as IODE_FILE_TYPES, IodeFileType as IodeFileType, IodeType as IodeType
from iode.iode_cython import CythonIodeDatabase as CythonIodeDatabase
from iode.util import JUSTIFY as JUSTIFY, check_filepath as check_filepath, join_lines as join_lines, split_list as split_list, table2str as table2str
from pathlib import Path
from typing import Any, Self

Self = Any

class PositionalIndexer:
    database: Incomplete
    def __init__(self, database) -> None: ...
    def __getitem__(self, index: int): ...
    def __setitem__(self, index: int, value): ...

class IodeDatabase:
    def __init__(self) -> None: ...
    @property
    def is_global_workspace(self) -> bool:
        '''
        Whether or not the present database represents the global IODE workspace.
        
        Returns
        -------
        bool

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.is_global_workspace
        True
        >>> cmt_copy = comments.copy()
        >>> cmt_copy.is_global_workspace
        False
        >>> cmt_subset = comments["A*"]
        >>> cmt_subset.is_global_workspace
        False
        '''
    @property
    def is_detached(self) -> bool:
        '''
        Whether or not any change made on the present database or subset will modify 
        the global IODE workspace.

        Returns
        -------
        bool

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> # \'comments\' represents the global Comments workspace
        >>> comments.is_detached
        False
        >>> comments["ACAF"]
        \'Ondernemingen: ontvangen kapitaaloverdrachten.\'

        >>> # by default, making a selection will create a new database 
        >>> # object that is a \'view\' of the global Comments workspace.
        >>> # Any change made on this \'view\' (subset) will also modify 
        >>> # the global workspace.
        >>> cmt_subset = comments["A*"]
        >>> cmt_subset.is_detached
        False
        >>> cmt_subset["ACAF"] = "modified comment"
        >>> cmt_subset["ACAF"]
        \'modified comment\'
        >>> comments["ACAF"]
        \'modified comment\'
        >>> # adding a new comment to the subset will also add it 
        >>> # to the global workspace
        >>> cmt_subset["NEW_CMT"] = "new comment"
        >>> "NEW_CMT" in comments
        True
        >>> comments["NEW_CMT"]
        \'new comment\'
        >>> # removing a comment from the subset will also remove it 
        >>> # from the global workspace
        >>> del cmt_subset["NEW_CMT"]
        >>> "NEW_CMT" in comments
        False

        >>> # explicitly calling the copy method will create a new 
        >>> # detached database. Any change made on the copy will not 
        >>> # modify the global workspace.
        >>> cmt_copy = comments["A*"].copy()
        >>> cmt_copy.is_detached
        True
        >>> cmt_copy["AOUC"] = "modified comment"
        >>> cmt_copy["AOUC"]
        \'modified comment\'
        >>> comments["AOUC"]
        \'Kost per eenheid produkt.\'
        '''
    def new_detached(self) -> Self:
        '''
        Create a new empty detached database.
        Here *detached* means that the new database is not linked to the global workspace. 
        Any change made to the *copied database* (*subset*) will not be applied to the global 
        workspace. This can be useful for example if you want to save previous values of scalars 
        before estimating an equation or a block of equations and then restore the original values 
        if the estimated values are not satisfying.
        
        Returns
        -------
        Database

        See Also
        --------
        IodeDatabase.copy

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> cmt_detached = comments.new_detached()
        >>> cmt_detached.is_detached
        True
        >>> cmt_detached.names
        []
        '''
    def copy(self, pattern: str = None) -> Self:
        '''
        Create a new database instance in which each object is a *copy* of the original object 
        from the global IODE database. Any change made to the *copied database* (*subset*) will 
        not be applied to the global workspace. This can be useful for example if you want to 
        save previous values of scalars before estimating an equation or a block of equations and 
        then restore the original values if the estimated values are not satisfying.

        Parameters
        ----------
        pattern : str, optional
            If provided, the copied database will only contain the objects whose name matches the 
            provided pattern. By default (None), the copied database will contain all the objects 
            from the global IODE database. The pattern syntax is the same as the one used for the 
            `__getitem__` method. If the pattern is an empty string, the copied database will be 
            empty, creating a new *detached* database.
            Default to None.

        Returns
        -------
        Database

        See Also
        --------
        IodeDatabase.new_detached
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 

        Database subset

        >>> # without using copy(), any modification made on 
        >>> # the subset will also change the corresponding 
        >>> # global IODE workspace
        >>> cmt_subset = comments["A*"]
        >>> cmt_subset.names
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\']
        >>> # a) add a comment
        >>> cmt_subset["A_NEW"] = "New comment"
        >>> "A_NEW" in cmt_subset
        True
        >>> "A_NEW" in comments
        True
        >>> comments["A_NEW"]
        \'New comment\'
        >>> # b) modify a comment
        >>> cmt_subset["ACAF"] = "Modified Comment"
        >>> cmt_subset["ACAF"]
        \'Modified Comment\'
        >>> comments["ACAF"]
        \'Modified Comment\'
        >>> # c) delete a comment
        >>> del cmt_subset["ACAG"]
        >>> "ACAG" in cmt_subset
        False
        >>> "ACAG" in comments
        False

        Copied database subset

        >>> cmt_subset_copy = comments["B*"].copy()
        >>> cmt_subset_copy.names
        [\'BENEF\', \'BENEF_\', \'BQY\', \'BVY\']
        >>> # or equivalently
        >>> cmt_subset_copy = comments.copy("B*")
        >>> cmt_subset_copy.names
        [\'BENEF\', \'BENEF_\', \'BQY\', \'BVY\']
        >>> # by using copy(), any modification made on the copy subset 
        >>> # let the global workspace unchanged
        >>> # a) add a comment -> only added in the copied subset
        >>> cmt_subset_copy["B_NEW"] = "New Comment"
        >>> "B_NEW" in cmt_subset_copy
        True
        >>> "B_NEW" in comments
        False
        >>> # b) modify a comment -> only modified in the copied subset
        >>> cmt_subset_copy["BENEF"] = "Modified Comment"
        >>> cmt_subset_copy["BENEF"]
        \'Modified Comment\'
        >>> comments["BENEF"]
        \'Ondernemingen: niet-uitgekeerde winsten.\'
        >>> # c) delete a comment -> only deleted in the copied subset
        >>> del cmt_subset_copy["BENEF_"]
        >>> "BENEF_" in cmt_subset_copy
        False
        >>> "BENEF_" in comments
        True

        New detached database

        >>> # a new empty *detached* database can be created by passing 
        >>> # an empty string to the copy() method 
        >>> cmt_detached = comments.copy("")
        >>> cmt_detached.names
        []
        >>> # or equivalently by using the new_detached() method 
        >>> cmt_detached = comments.new_detached()
        >>> cmt_detached.names
        []
        '''
    @property
    def iode_type(self) -> IodeType:
        '''
        Return the object type of the current database.

        Returns
        -------
        IodeType

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.iode_type
        <IodeType.COMMENTS: 0>
        '''
    @property
    def filename(self) -> str:
        '''
        Return the filepath associated with the current database.

        Returns
        -------
        str

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> from pathlib import Path
        >>> from os.path import relpath
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> filename = comments.filename
        >>> Path(filename).name
        \'fun.cmt\'
        >>> comments.filename = "new_filename.cmt"
        >>> filename = comments.filename
        >>> Path(filename).name
        \'new_filename.cmt\'
        '''
    @filename.setter
    def filename(self, value: str): ...
    @property
    def description(self) -> str:
        '''
        Description of the current database.

        Parameters
        ----------
        value: str
            New description.
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.description = "test data from file \'fun.cmt\'"
        >>> comments.description
        "test data from file \'fun.cmt\'"
        '''
    @description.setter
    def description(self, value: str): ...
    def get_position(self, name: str) -> int:
        '''
        Return the position of the IODE object with name `name` in the database.

        Parameters
        ----------
        name: str
            Name of the IODE object to search for in the database.
        
        Returns
        -------
        int

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.get_position("ACAF")
        0
        '''
    def get_name(self, pos: int) -> str:
        '''
        Return the name of the IODE object at position `pos` in the database.

        Parameters
        ----------
        pos: int
           Position of the object in the database.

        Returns
        -------
        str

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.get_name(0)
        \'ACAF\'
        '''
    def get_names(self, pattern: str | list[str] = None, filepath: str | Path = None) -> list[str]:
        '''
        Returns the list of objects names given a pattern.
        If a file is provided, search for names in the file instead of the current database.

        Parameters
        ----------
        pattern: str or list(str), optional
            pattern to select a subset of objects. 
            For example, \'A*;*_\' will select all objects for which the name starts 
            with \'A\' or ends with \'_\'.
            Return all names contained in the database by default.
        filepath: str or Path, optional
            Path to the file to search for names. 
            Search in the current database by default.

        Returns
        -------
        list(str)
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.get_names("A*;*_")         # doctest: +NORMALIZE_WHITESPACE
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\', \'BENEF_\', \'GOSH_\', 
        \'IDH_\', \'PAFF_\', \'PC_\', \'PFI_\', \'QAFF_\', \'QAF_\', 
        \'QAI_\', \'QAT_\', \'QBBPPOT_\', \'QC_\', \'QQMAB_\', \'QS_\', 
        \'Q_\', \'TFPHP_\', \'VAFF_\', \'VAI_\', \'VAT_\', \'VC_\', \'VS_\', 
        \'WBF_\', \'WBU_\', \'WCF_\', \'WCR1_\', \'WCR2_\', \'WIND_\', 
        \'WNF_\', \'YDH_\', \'ZZ_\']
        >>> # or equivalently
        >>> comments.get_names(["A*", "*_"])    # doctest: +NORMALIZE_WHITESPACE
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\', \'BENEF_\', \'GOSH_\', 
        \'IDH_\', \'PAFF_\', \'PC_\', \'PFI_\', \'QAFF_\', \'QAF_\', 
        \'QAI_\', \'QAT_\', \'QBBPPOT_\', \'QC_\', \'QQMAB_\', \'QS_\', 
        \'Q_\', \'TFPHP_\', \'VAFF_\', \'VAI_\', \'VAT_\', \'VC_\', \'VS_\', 
        \'WBF_\', \'WBU_\', \'WCF_\', \'WCR1_\', \'WCR2_\', \'WIND_\', 
        \'WNF_\', \'YDH_\', \'ZZ_\']
        >>> # get the list of all names
        >>> comments.names                # doctest: +ELLIPSIS
        [\'ACAF\', \'ACAG\', \'AOUC\', ..., \'ZKF\', \'ZX\', \'ZZ_\']
        >>> # search in file
        >>> comments.clear()
        >>> comments.get_names("A*;*_")
        []
        >>> comments.get_names("A*;*_", f"{SAMPLE_DATA_DIR}/fun.cmt")   # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading ...\\fun.cmt
        317 objects loaded
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\', \'BENEF_\', \'GOSH_\', 
        \'IDH_\', \'PAFF_\', \'PC_\', \'PFI_\', \'QAFF_\', \'QAF_\', 
        \'QAI_\', \'QAT_\', \'QBBPPOT_\', \'QC_\', \'QQMAB_\', \'QS_\', 
        \'Q_\', \'TFPHP_\', \'VAFF_\', \'VAI_\', \'VAT_\', \'VC_\', \'VS_\', 
        \'WBF_\', \'WBU_\', \'WCF_\', \'WCR1_\', \'WCR2_\', \'WIND_\', 
        \'WNF_\', \'YDH_\', \'ZZ_\']
        >>> # empty pattern -> return no names
        >>> comments.get_names("")
        []
        '''
    def get_names_from_pattern(self, list_name: str, pattern: str, xdim: str | list[str], ydim: str | list[str] = None) -> list[str]:
        '''
        Generate an IODE list containing the names of objects that match a given pattern.

        Parameters
        ----------
        list_name: str
            Name of the IODE list which will contain the resulting list of names.
        pattern: str
            Pattern to which the name of the objects must conform, where "x" is replaced by 
            the elements from \'xdim\' and, if specified, "y" by the elements from \'ydim\'.
        xdim: str or list(str)
            x dimension of the list. It can be a list of strings or an existing IODE list.
            If it is an existing IODE list, it must be referred as "$<list_name>". 
        ydim: str or list(str), optional
            y dimension of the list. It can be a list of strings or an existing IODE list.
            If it is an existing IODE list, it must be referred as "$<list_name>". 
            Defaults to None.

        Returns
        -------
        list(str)
        
        Examples
        --------
        >>> import numpy as np
        >>> from iode import variables, lists
        >>> # fill the variables database
        >>> variables.sample = "2000Y1:2010Y1"
        >>> variables["R1C1"] = np.nan
        >>> variables["R1C2"] = np.nan
        >>> variables["R1C3"] = np.nan
        >>> variables["R2C1"] = np.nan
        >>> variables["R2C2"] = np.nan
        >>> variables["R2C3"] = np.nan
        >>> variables["R3C1"] = np.nan
        >>> variables["R3C2"] = np.nan
        >>> variables["R3C3"] = np.nan
        >>> # create an IODE list X
        >>> lists["X"] = ["R1", "R2", "R3"]
        >>> # create an IODE list Y
        >>> lists["Y"] = ["C1", "C2", "C3"]
        >>> # generate the IODE list of variables names 
        >>> # given a pattern
        >>> variables.get_names_from_pattern("RC", "xy", "$X", "$Y")
        [\'R1C1\', \'R1C2\', \'R1C3\', \'R2C1\', \'R2C2\', \'R2C3\', \'R3C1\', \'R3C2\', \'R3C3\']
        >>> lists["RC"]
        [\'R1C1\', \'R1C2\', \'R1C3\', \'R2C1\', \'R2C2\', \'R2C3\', \'R3C1\', \'R3C2\', \'R3C3\']
        '''
    @property
    def names(self) -> list[str]:
        '''
        List of names of all objects in the current database.

        Returns
        -------
        list(str)
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> # get the list of all names
        >>> comments.names                # doctest: +ELLIPSIS
        [\'ACAF\', \'ACAG\', \'AOUC\', ..., \'ZKF\', \'ZX\', \'ZZ_\']
        '''
    def rename(self, old_name: str, new_name: str):
        '''
        Rename an object of the database.

        Parameters
        ----------
        old_name: str
            current name in the database
        new_name: str
            new name in the database

        Warning
        -------
        Renaming an Equation is not allowed.
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments["ACAF"]
        \'Ondernemingen: ontvangen kapitaaloverdrachten.\'

        >>> # rename comment \'ACAF\' as \'ACCAF\'
        >>> comments.rename("ACAF", "ACCAF")
        >>> "ACCAF" in comments
        True
        >>> comments["ACCAF"]
        \'Ondernemingen: ontvangen kapitaaloverdrachten.\'
        '''
    def remove(self, names: str | list[str]):
        '''
        Delete the object(s) named \'names\' from the current database.
        
        Parameters
        ----------
        names: str
            name(s) of object(s) to be deleted. 
            It can be a pattern (e.g. "A*").

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> comments.get_names("A*")
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\']

        >>> # remove one object
        >>> comments.remove("ACAF")
        >>> comments.get_names("A*")
        [\'ACAG\', \'AOUC\', \'AQC\']

        >>> # remove all objects with a name ending by \'_\'
        >>> comments.get_names("*_")            # doctest: +ELLIPSIS
        [\'BENEF_\', \'GOSH_\', \'IDH_\', ..., \'WNF_\', \'YDH_\', \'ZZ_\']
        >>> comments.remove("*_")
        >>> comments.get_names("*_")
        []
        '''
    def compare(self, filepath: str | Path, only_in_workspace_list_name: str = None, only_in_file_list_name: str = None, equal_objects_list_name: str = None, different_objects_list_name: str = None) -> dict[str, list[str]]:
        '''
        The objects of the current database are compared with those stored in the file `filepath`. 
        
        The result of this comparison is composed of 4 lists:
        
          - *only_in_workspace_list*: objects only found in the current database
          - *only_in_file_list*: objects only found in the file `filepath`
          - *equal_objects_list*: objects found in both with the same value
          - *different_objects_list*: objects found in both but with a different value
        
        The comparison is made according to current database type.

        For the IODE Variables, the comparison between two variables is made according to 
        the threshold defined by :meth:`iode.Variables.threshold`.

        Parameters
        ----------
        filepath: str or Path
            path to the file to be compared with the current database
        only_in_workspace_list_name: str, optional
            name of the list of objects only found in the current database.
            Defaults to "OLD_<IODE_TYPE>".
        only_in_file_list_name: str, optional
            name of the list of objects only found in the file `filepath`.
            Defaults to "NEW_<IODE_TYPE>".
        equal_objects_list_name: str, optional
            name of the list of objects found in both with the same value.
             Defaults to "SAME_<IODE_TYPE>".
        different_objects_list_name: str, optional
            name of the list of objects found in both but with a different value.
            Defaults to "CHANGED_<IODE_TYPE>".

        Returns
        -------
        dict(str, list(str))
            dictionary containing the 4 lists of objects

        Examples
        --------
        >>> import numpy as np
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import variables
        >>> output_dir = getfixture(\'tmp_path\')

        >>> variables.load(f"{SAMPLE_DATA_DIR}/fun.var")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading ...fun.var
        394 objects loaded
        >>> variables.threshold
        1e-07

        >>> # ---- create Variables file to compare with ----
        >>> vars_other_filepath = str(output_dir / "fun_other.var")
        >>> vars_other = variables.copy()
        >>> # add two variables
        >>> vars_other["NEW_VAR"] = 0.0
        >>> vars_other["NEW_VAR_2"] = 0.0
        >>> # delete two variables
        >>> del vars_other["AOUC"]
        >>> del vars_other["AQC"]
        >>> # change the value of two variables (above threshold)
        >>> vars_other["ACAF"] = "ACAF + 1.e-5"
        >>> vars_other["ACAG"] = "ACAG + 1.e-5"
        >>> # change the value of two variables (below threshold)
        >>> vars_other["BENEF"] = "BENEF + 1.e-8"
        >>> vars_other["BQY"] = "BQY + 1.e-8"
        >>> # save the Variables file to compare with
        >>> vars_other.save(vars_other_filepath)                    # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Saving ...fun_other.var
        394 objects saved

        >>> # ---- compare the current Variables database ----
        >>> # ---- with the content of the saved file     ----
        >>> lists_compare = variables.compare(vars_other_filepath)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading ...fun_other.var
        394 objects loaded
        >>> for name, value in lists_compare.items():           # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        ...    print(f"{name}: {value}")
        OLD_VAR: [\'AOUC\', \'AQC\']
        NEW_VAR: [\'NEW_VAR\', \'NEW_VAR_2\']
        SAME_VAR: [\'AOUC_\', \'BENEF\', \'BQY\', \'BRUGP\', ..., \'ZKFO\', \'ZX\', \'ZZF_\'] 
        CHANGED_VAR: [\'ACAF\', \'ACAG\']
        '''
    def merge(self, other: Self, overwrite: bool = True):
        '''
        Merge the content of the \'other\' database into the current database.

        Parameters
        ----------
        other:
            other database to be merged in the current one.
        overwrite: bool, optional
            Whether or not to overwrite the objects with the same name in the two database.
            Defaults to True.
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")     # doctest: +ELLIPSIS
        Loading .../fun.cmt
        317 objects loaded

        >>> # copy comments with names starting with \'A\' into a 
        >>> # new database \'cmt_detached\'
        >>> cmt_detached = comments.copy("A*")
        >>> cmt_detached.names
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\']

        >>> # remove \'ACAF\' and \'ACAG\' from the global Comments database
        >>> del comments[\'ACAF;ACAG\']
        >>> comments.get_names("A*")
        [\'AOUC\', \'AQC\']

        >>> # update the content of \'AOUC\' in \'cmt_detached\'
        >>> cmt_detached[\'AOUC\'] = "Comment modified"
        >>> cmt_detached[\'AOUC\']
        \'Comment modified\'
        >>> # content of \'AOUC\' in the global Comments database
        >>> comments[\'AOUC\']
        \'Kost per eenheid produkt.\'

        >>> # merge \'cmt_detached\' into the global Comments database
        >>> # -> preserve \'AOUC\' in the global Comments database
        >>> comments.merge(cmt_detached, overwrite=False)
        >>> \'ACAF\' in comments
        True
        >>> \'ACAG\' in comments
        True
        >>> comments[\'AOUC\']
        \'Kost per eenheid produkt.\'

        >>> # merging \'cmt_detached\' into the global Comments database
        >>> # -> overwrite the content of \'AOUC\' in the global Comments database 
        >>> comments.merge(cmt_detached)
        >>> comments[\'AOUC\']
        \'Comment modified\'
        '''
    def merge_from(self, input_file: str):
        '''
        Merge all objects stored in the input file \'input_file\' into the current database.

        Parameters
        ----------
        input_file: str
            file from which the objects to merge are read.
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")         # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded
        >>> len(comments)
        317
        >>> # delete all comments
        >>> comments.clear()
        >>> len(comments)
        0

        >>> # reload all comments
        >>> comments.merge_from(f"{SAMPLE_DATA_DIR}/fun.cmt")   # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading ...\\fun.cmt
        317 objects loaded
        >>> len(comments)
        317
        '''
    def search(self, pattern: str, word: bool = True, case_sensitive: bool = True, in_name: bool = True, in_formula: bool = True, in_text: bool = True, list_result: str = '_RES') -> list[str]:
        '''
        Return a list of all objects from the current database having a specific pattern in their names or LEC expression, comment...
          
        The following characters in *pattern* have a special meaning:
        
            - `*` : any character sequence, even empty
            - `?` : any character (one and only one)
            - `@` : any alphanumerical char [A-Za-z0-9]
            - `&` : any non alphanumerical char
            - `|` : any alphanumeric character or none at the beginning and end of a string 
            - `!` : any non-alphanumeric character or none at the beginning and end of a string 
            - `\\` : escape the next character
        
        The Search method depends on the type of object:

        - Comments: the name and text of the comments are analyzed 
        - Equations: the name and LEC form of the equations are analyzed 
        - Identities: the name and LEC form of the identities are analyzed 
        - Lists: the name and text of the lists are analyzed 
        - Scalars: the name of the scalars is analyzed 
        - Tables: the table name, titles and LEC forms are analyzed 
        - Variables: the name of the variables is analyzed 

        Parameters
        ----------
        pattern: str     
            string to search
        word: bool, optional
            Whether or not the pattern to be searched for must be a whole word and not part of a word. 
            Default to True.
        case_sensitive: bool, optional
            Whether or not the search is case sensitive.
            Default to True.
        in_name: bool, optional
            Whether or not to also search in object names.
            Default to True.
        in_formula: bool, optional
            Whether or not to also search in LEC expressions (for Equations, Identities and Tables (LEC cells)).
            Default to True.
        in_text: bool, optional
            Whether or not to also search in texts (for Comments, lists, Equations (comment) and Tables (text cells)).
            Default to True.
        list_result: str, optional
            Name of the IODE list in which the resulting list of objects is saved.
            Default to *_RES*.

        Returns
        -------
        list(str)

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments, equations, identities, lists, tables
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")         # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> equations.load(f"{SAMPLE_DATA_DIR}/fun.eqs")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.eqs
        274 objects loaded 
        >>> identities.load(f"{SAMPLE_DATA_DIR}/fun.idt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.idt
        48 objects loaded 
        >>> lists.load(f"{SAMPLE_DATA_DIR}/fun.lst")            # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.lst
        17 objects loaded 
        >>> tables.load(f"{SAMPLE_DATA_DIR}/fun.tbl")           # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.tbl
        46 objects loaded 

        >>> # get list of comments containing \'Bruto\'
        >>> comments.search("Bruto")            # doctest: +ELLIPSIS 
        [\'GOSF\', \'GOSG\', \'GOSH\', \'GOSH_\', ..., \'VIF\', \'VIG\', \'YDH\', \'YDH_\']

        >>> # get list of equations containing \'AOUC\'
        >>> equations.search("AOUC")
        [\'AOUC\', \'PC\', \'PIF\', \'PXS\', \'QXAB\']

        >>> # get list of identities containing \'NDOMY\'
        >>> identities.search("NDOMY")
        [\'LCLASS\', \'LKEYN\', \'UCLASS\']

        >>> # get list of IODE lists containing \'AOUC\'
        >>> lists.search("AOUC")
        [\'COPY0\', \'ENDO0\', \'TOTAL0\']

        >>> # get list of IODE tables containing \'AOUC\' in cells
        >>> tables.search("AOUC")
        [\'ANAPRIX\', \'MULT1FR\', \'MULT1RESU\', \'T1\', \'T1NIVEAU\']
        '''
    def print_to_file(self, filepath: str | Path, names: str | list[str] = None, format: str = None): ...
    def print_to_file(self, filepath: str | Path, names: str | list[str] = None, format: str = None): ...
    def load(self, filepath: str):
        '''
        Load objects stored in file \'filepath\' into the current database.
        Erase the database before to load the file.

        Parameters
        ----------
        filepath: str
            path to the file to load
        
        Examples
        --------
        >>> from iode import comments, equations, identities, lists, tables, scalars, variables
        >>> from iode import SAMPLE_DATA_DIR
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")         # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded
        
        >>> equations.load(f"{SAMPLE_DATA_DIR}/fun.eqs")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.eqs
        274 objects loaded
        
        >>> identities.load(f"{SAMPLE_DATA_DIR}/fun.idt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.idt
        48 objects loaded
        
        >>> lists.load(f"{SAMPLE_DATA_DIR}/fun.lst")            # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.lst
        17 objects loaded
        
        >>> tables.load(f"{SAMPLE_DATA_DIR}/fun.tbl")           # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.tbl
        46 objects loaded
        
        >>> scalars.load(f"{SAMPLE_DATA_DIR}/fun.scl")          # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.scl
        161 objects loaded
        
        >>> variables.load(f"{SAMPLE_DATA_DIR}/fun.var")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.var
        394 objects loaded
        '''
    def save(self, filepath: str, compress: bool = False):
        '''
        Save objects of the current database into the file \'filepath\'.

        Parameters
        ----------
        filepath: str
            path to the file to save.
        compress: bool, optional
            Whether or not to compress the file. 
            If True, the file will be written using the LZH compression algorithm.
            This may slow down the writing process but will reduce the size of the saved file.
            Default to False.
        
        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")         # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> len(comments)
        317
        >>> comments.save(f"{SAMPLE_DATA_DIR}/fun2.cmt")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Saving .../fun2.cmt
        317 objects saved
        >>> comments.clear()
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun2.cmt")        # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun2.cmt
        317 objects loaded
        >>> len(comments)
        317
        '''
    def clear(self) -> None:
        '''
        Delete all objects from the current database.

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> len(comments)
        317
        >>> comments.clear()
        >>> len(comments)
        0
        '''
    def __len__(self) -> int:
        '''
        Return the number of IODE objects in the current database.

        Returns
        -------
        int

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> len(comments)
        317
        '''
    def __contains__(self, item) -> bool:
        '''
        Test if the IODE object named `item` is present in the current database.

        Parameters
        ----------
        item: str
            name of the IODE object. 

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> "ACAF" in comments
        True
        >>> "ZCAF" in comments
        False
        '''
    def __iter__(self):
        '''
        Iterate over object names.

        Examples
        --------
        >>> from iode import SAMPLE_DATA_DIR
        >>> from iode import comments
        >>> comments.load(f"{SAMPLE_DATA_DIR}/fun.cmt")       # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        Loading .../fun.cmt
        317 objects loaded 
        >>> cmt_subset = comments["A*"]
        >>> cmt_subset.names
        [\'ACAF\', \'ACAG\', \'AOUC\', \'AQC\']
        >>> for name in cmt_subset:
        ...     print(name)
        ACAF
        ACAG
        AOUC
        AQC
        '''
    @property
    def i(self) -> PositionalIndexer: ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    def __delitem__(self, key) -> None: ...
    def __hash__(self) -> int: ...
