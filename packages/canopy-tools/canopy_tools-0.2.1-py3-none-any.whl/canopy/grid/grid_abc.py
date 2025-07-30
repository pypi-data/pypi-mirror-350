from typing_extensions import Self
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import pandas as pd

class Grid(ABC):
    """Abstract base class for a generic Grid object

    A grid object describes the grid associated to the data in a Field object.
    """

    def __init__(self,
                 grid_type: str,
                 axis0: str, axis1: str,
                 gridop0: str | None = None, gridop1: str | None = None):
        """The Grid superclass constructor

        Parameters
        ----------
        axis0
            The name of the first axis (e.g. 'x' or 'lon').
        axis1
            The name of the second axis (e.g. 'y' or 'lat').
        """
        self._grid_type = grid_type
        self._axis_names: tuple = (axis0, axis1)
        self._axis_gridop: dict['str','str' | None] = {name: gridop for name, gridop in zip(self.axis_names, [gridop0, gridop1])}


    @property
    def grid_type(self):
        return self._grid_type

    @property
    def axis_names(self):
        return self._axis_names

    @property
    def axis_gridop(self):
        return self._axis_gridop

    @classmethod
    @abstractmethod
    def from_frame(cls, df: pd.DataFrame) -> Self:
        """Create a grid from a DataFrame.

        The method should construct a grid object of the subclassed type with the information
        from the pandas DataFrame. For an example, see the Grid subclasses defined in the grid/
        folder (files grid_sites.py, ...)

        Parameters
        ----------
        df
            A pandas DataFrame with a valid format (see Field documentation).

        Returns
        -------
        An instance of the grid subclass.
        """
        pass

    @abstractmethod
    def get_sliced_grid(self, axis0_slice: tuple[float,float] | None, axis1_slice: tuple[float,float] | None) -> 'Grid':
        """Create a new grid, sliced accordingto the parameters

        Parameters
        ----------
        axis0_slice
            Specifies an interval on axis0.
        axis1_slice
            Specifies an interval on axis1.

        Returns
        -------
        An instance of the grid subclass.
        """
        pass

    @abstractmethod
    def get_reduced_grid(self, gridop: str, axis: str) -> 'Grid':
        """Create a new grid, reduced according to the parameters

        Parameters
        ----------
        gridop
            The reduction operation
        axis
            The axis to be reduced

        Returns
        -------
        An instance of the grid subclass

        Notes
        -----
        This function has two responsibilities:
            To change the value of `self.axis_gridop`:
                self.axis_gridop[axis] = gridop
                
            To 'collapse' the reduced axis. For example, if the reduction
            is along the 'x' axis, replace the representation of this axis by
            some placehoder value, like `None` or `np.empty[]`. The concrete
            implementation will depend on how axes are represented in the specific
            Grid subclass.
        """
        pass

    def is_reduced(self, axis: str) -> bool:
        """Check whether axis has been reduced.

        Parameters
        ----------
        axis
            The name or index of the axis to check.

        Returns
        -------
            A boolean: True if the axis has been reduced, False otherwise.
        """
        if isinstance(axis, int):
            axis = self.axis_names[axis]

        return self.axis_gridop[axis] is not None


