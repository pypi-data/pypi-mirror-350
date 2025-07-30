from collections.abc import Sequence
import os
import pathlib
from typing import Annotated, overload

from numpy.typing import ArrayLike
import pandas

import hictkpy
import hictkpy._hictkpy


class FileWriter:
    """Class representing a file handle to create .hic files."""

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolution: int, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one resolution.
        """

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolutions: Sequence[int], assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one or more resolutions.
        """

    @overload
    def __init__(self, path: str | os.PathLike, bins: hictkpy._hictkpy.BinTable, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a BinTable. Only BinTable with a fixed bin size are supported.
        """

    def __repr__(self) -> str: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def resolutions(self) -> Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C')]:
        """Get the list of resolutions in bp."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def bins(self, resolution: int) -> hictkpy.BinTable:
        """Get table of bins for the given resolution."""

    def add_pixels(self, pixels: pandas.DataFrame, validate: bool = True) -> None:
        """
        Add pixels from a pandas DataFrame containing pixels in COO or BG2 format (i.e. either with columns=[bin1_id, bin2_id, count] or with columns=[chrom1, start1, end1, chrom2, start2, end2, count].
        When validate is True, hictkpy will perform some basic sanity checks on the given pixels before adding them to the .hic file.
        """

    def finalize(self, log_lvl: str = 'WARN') -> hictkpy._hictkpy.File:
        """Write interactions to file."""

