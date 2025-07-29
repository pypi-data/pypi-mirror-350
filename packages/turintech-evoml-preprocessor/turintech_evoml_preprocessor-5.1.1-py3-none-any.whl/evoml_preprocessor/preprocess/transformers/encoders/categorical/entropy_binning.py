"""This module provides EntropyBinningEncoder class for encoding special categorical columns."""

# ─────────────────────────────────────────── imports ─────────────────────────────────────────── #
# Standard Library
from typing import Set, Dict, Optional

# 3rd Party
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

# Dependencies
from evoml_utils.convertors.special_categorical.convertor import convert_special_categorical_column
from evoml_utils.range import Range, RangeType
from evoml_utils.binning import KmeansIntegerArrayBinning, DynamicIntegerArrayBinning

# ──────────────────────────────────────────── Code ──────────────────────────────────────────── #


class EntropyBinning:
    """This class provides methods for encoding special categorical columns.

    Important:
    This class is made only for encoding special categorical columns. It is not
    meant to be used for encoding normal categorical or other types of columns.
    If you want to bin an array of integers, use the evoml_utils.binning
    methods directly.

    When a special categorical column is given, the encoder first converts
    it to a 1-d array of Range objects. Then, it replaces all points inside
    rays and intervals with the corresponding rays and intervals.
    Then, the array is sorted and encoded using OrdinalEncoder.
    Finally, the array is binned using IntegerArrayBinning class from
    evoml_utils.binning module.

    Attributes:
        _bins (Optional[np.ndarray]): the optimal binning found during fitting.
        _number_of_unique_rays_and_intervals (Optional[int]):
            the number of unique rays and intervals,

    Methods:
        fit_transform(data: pd.Series) -> np.ndarray:
            fit_transform function of the EntropyBinningEncoder class.

            Encodes the special categorical column to a 1-d array of integers.
            Bins not nan values of the special categorical column to bins [1, ..., n],
                where n is the optimal number of bins calculated:
                n = max(log len(data \\ nan values), # of rays and intervals)
            All nan values are put in bin 0.

        transform(data: pd.Series) -> np.ndarray:
            transform function. Requires `fit_transform` to be run first.
            Is able to handle unseen data.

    """

    def __init__(self):
        self._bins: Optional[np.ndarray] = None
        self._number_of_unique_rays_and_intervals: Optional[int] = None

    def fit_transform(self, data: pd.Series) -> np.ndarray:
        """fit_transform function of the Entropy Binning Ordinal Encoder class.

        Bins not nan values of the special categorical column to bins [1, ..., n],
            where n is the optimal number of bins calculated:
            n = max(log len(data \\ nan values), # of rays and intervals)

        All nan values are put in bin 0.

        Sets self._bins to the optimal binning found while fitting the data.

        Args:
            data (pd.Series): the column to fit_transform.

        Returns:
            labels (np.ndarray): 1-d array with transformed values.

        """

        if (data_length := data.shape[0]) == 0:
            self._bins = np.array([Range(start=np.NINF, end=np.inf)])
            return data.to_numpy()

        # ------------------------------------ Prepare data ------------------------------------ #

        _, ranges = convert_special_categorical_column(data)
        ranges = ranges.to_numpy()

        # replace rays that intercept and points inside rays and intervals
        ranges = self._replace_inner_points(ranges)

        # ------------------------------------- Bin ranges ------------------------------------- #

        labels = np.empty(data_length, dtype=int)
        converted_null_map = pd.isnull(ranges)  # pd.isnull handles nans
        labels[~converted_null_map] = self._bin_ranges(ranges[~converted_null_map]) + 1
        labels[converted_null_map] = 0

        return labels

    def transform(self, data: pd.Series) -> np.ndarray:
        """transform function. Requires `fit_transform` to be run first.
        Is able to handle unseen data.

        Bins not nan values of the special categorical column to bins [1, ..., n],
        based on the optimal binning found during fitting.

        All nan values are put in bin 0.

        Args:
            data (pd.Series): the column to transform.

        Returns:
            binned (np.ndarray): 1-d array with transformed values.

        Raises:
            ValueError: if `fit_transform` was not run first.

        """

        if data.shape[0] == 0:
            return data.to_numpy()

        if self._bins is None:
            raise ValueError("Must run fit_transform first.")

        # ------------------------------------ Prepare data ------------------------------------ #

        _, ranges = convert_special_categorical_column(data)
        ranges = ranges.to_numpy()

        # ------------------------------------- Bin ranges ------------------------------------- #

        labels = np.zeros(ranges.shape, dtype=int)
        for i, range_ in enumerate(ranges):

            # if nan, put in bin 0
            if not isinstance(range_, Range):
                continue

            # if not nan, bin
            for j, bin_ in enumerate(self._bins, start=1):
                if bin_.includes(range_.centre()):
                    labels[i] = j
                    break

        return labels

    @staticmethod
    def _ordinal_encode(ranges: np.ndarray) -> np.ndarray:
        """Input sorted array of Range obj. Output OrdinalEncoded"""
        encoder = OrdinalEncoder()
        return np.ravel(encoder.fit_transform(ranges.reshape(-1, 1))).astype(np.int64)

    def _optimal_number_of_bins(self, number_of_ranges: int, number_of_unique_ranges_: int) -> int:
        """Finds the optimal number of bins for binning.

        Optimal is: log len(ranges). But cannot be smaller than the number of
        unique rays and intervals; And cannot be larger than the number
        of unique ranges."""

        max_ = int(np.log(number_of_ranges))
        min_ = self._number_of_unique_rays_and_intervals
        if min_ is None:
            raise ValueError("Minimum number of unique rays and intervals should be set by fitting the encoder.")
        return min(max(min_, max_), number_of_unique_ranges_)

    def _bin_ranges(self, ranges: np.ndarray) -> np.ndarray:
        """Bins ranges to bins [0, ..., n - 1], where n is the optimal number of bins"""

        unique_ranges = pd.unique(ranges)
        if not isinstance(unique_ranges, np.ndarray):
            raise TypeError(f"Expected np.ndarray, got {type(unique_ranges)}")
        number_of_unique_ranges = unique_ranges.shape[0]
        n_bins = self._optimal_number_of_bins(ranges.shape[0], number_of_unique_ranges)

        # ------------------------------------ Prepare data ------------------------------------ #

        arg_sorted = np.argsort(ranges)
        sorted_ranges = ranges[arg_sorted]
        ord_encoded = self._ordinal_encode(sorted_ranges)

        # ------------------------------------ Bin the data ------------------------------------ #

        if n_bins < number_of_unique_ranges:
            if number_of_unique_ranges < 10_000:  # below 10_000, dynamic is faster
                iab = DynamicIntegerArrayBinning(n_bins=n_bins)
            else:
                iab = KmeansIntegerArrayBinning(n_bins=n_bins)

            sorted_labels = iab.fit_transform(ord_encoded)

        else:
            sorted_labels = ord_encoded

        labels = np.empty(ranges.shape[0], dtype=int)
        labels[arg_sorted] = sorted_labels  # unsort

        # ---------------------------------- Save the binning ---------------------------------- #

        bin_starts = sorted_ranges[np.where(np.diff(sorted_labels) > 0)[0] + 1]  # first bin is not included
        bin_ends = sorted_ranges[np.where(np.diff(sorted_labels) > 0)[0]]  # last bin is not included

        # create an array of Ranges, where each Range represents a bin. Bins change at midpoints.
        if np.any(midpoints := np.array([Range.midpoint(start, end) for start, end in zip(bin_starts, bin_ends)])):
            self._bins = np.concatenate(
                [
                    [Range(start=np.NINF, end=midpoints[0].num, start_inclusive=False, end_inclusive=False)],
                    [
                        Range(
                            start=midpoints[i].num, end=midpoints[i + 1].num, start_inclusive=True, end_inclusive=False
                        )
                        for i in range(midpoints.shape[0] - 1)
                    ],
                    [Range(start=midpoints[-1].num, end=np.inf, start_inclusive=True, end_inclusive=False)],
                ]
            )
        else:  # number of bins is 1
            self._bins = np.array([Range(start=np.NINF, end=np.inf)])

        return labels

    def _replace_inner_points(self, ranges: np.ndarray) -> np.ndarray:
        """This function replaces all points inside rays and intervals
        with the corresponding rays and intervals.

        Saves the number of unique rays and intervals in
            self._number_of_unique_rays_and_intervals.

        Args:
            ranges (np.ndarray): array of Range objects.

        Returns:
            ranges (np.ndarray): array of Range objects, with all
                points being outside the rays and intervals.

        """

        # points inside rays and intervals transform to corresponding rays and intervals.
        unique_rays_intervals: Set[Range] = {
            range_ for range_ in ranges if isinstance(range_, Range) and range_.type != RangeType.POINT
        }
        replace_points: Dict[Range, Range] = {}
        for point in {point for point in ranges if isinstance(point, Range) and point.type == RangeType.POINT}:
            for ray_or_interval in unique_rays_intervals:
                if ray_or_interval.includes(point):
                    replace_points[point] = ray_or_interval
                    break

        # update points
        for key, value in replace_points.items():
            ranges[ranges == key] = value

        # save the number of unique rays and intervals
        self._number_of_unique_rays_and_intervals = len(unique_rays_intervals)

        return ranges
