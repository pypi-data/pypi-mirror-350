from __future__ import annotations

import itertools
from typing import Iterator, Set, List, Dict

import numpy as np
from numpy.typing import NDArray
import pandas as pd

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode


class FeatureGenerationPool:
    """Feature generation pool, which acts like a set of `GeneratedFeatureNode`

    The pool has a few additional capabilities:
    - memory, which ensures new features must have not been generated before.
    - regeneration, which allows the pool to populate itself with a set of
    features each epoch.

    It stores a few additional sets to enable these capabilities:
    - `_cache` (Set[int]): The hashed `GeneratedFeatureNode` objects that have
        been created before.
    - `_names` (Set[str]): The names of `GeneratedFeatureNode` objects that
        have been created before.
    - `_regenerate` (Set[GeneratedFeatureNode]): The set of nodes to add to
        the pool on `regenerate`.
    - `_pool` (Set[GeneratedFeatureNode]): The set of generated features
        exposed to external entities.
    - `_ordered_pool` (List[GeneratedFeatureNode]): A list of ordered features
        populated if `lock` is called and depopulated whenever the `_pool` is
        altered.
    """

    _cache: Set[int]
    _names: Set[str]
    _regenerate: Set[GeneratedFeatureNode]
    _pool: Set[GeneratedFeatureNode]
    _ordered_pool: List[GeneratedFeatureNode]

    # BUILD

    def __init__(self) -> None:
        self._cache = set()
        self._names = set()
        self._regenerate = set()
        self._pool = set()
        self._ordered_pool = []

    def add_regenerated_feature(self, feature: pd.Series[float]) -> None:
        """Add a single feature (as a pandas column) to be regenerated.

        The cache ensures that this regenerated feature cannot be added
        to the pool via an `add_generated_feature` call.

        Args:
            feature (pd.Series):
                the feature to add to the regenerated set of features
        """
        gf = GeneratedFeatureNode.from_feature(feature)
        self._regenerate.add(gf)
        self._ordered_pool.clear()
        self.cache_generated_feature(gf)

    def add_feature(self, feature: pd.Series[float]) -> None:
        """Add a single feature (as a pandas column) to the pool.

        The cache ensures that this feature cannot be added again to the
        pool via an `add_generated_feature` call.

        Args:
            feature (pd.Series):
                the feature to add to the pool of features
        """
        gf = GeneratedFeatureNode.from_feature(feature)
        self._pool.add(gf)
        self._ordered_pool.clear()
        self.cache_generated_feature(gf)

    def add_generated_feature(self, feature: GeneratedFeatureNode) -> None:
        """Add a generated feature to the pool.

        Behaves like the `add` method from `Set` with an additional check
        for cached results.

        Args:
            feature (GeneratedFeatureNode):
                feature to add
        """
        if feature not in self:
            self._pool.add(feature)
        self._ordered_pool.clear()
        self.cache_generated_feature(feature)

    def remove_generated_feature(self, feature: GeneratedFeatureNode) -> None:
        """Remove a generated feature to the pool.

        NOTE: without resetting the cache, this feature cannot be readded!

        Args:
            feature (GeneratedFeatureNode):
                feature to remove
        """
        self._ordered_pool.clear()
        if feature in self._pool:
            self._pool.remove(feature)

    # REPRESENTATIONS

    def __str__(self) -> str:
        return "{" + "; ".join([repr(f) for f in self._pool]) + "}"

    def __repr__(self) -> str:
        return self.__str__()

    # ACCESS

    def lock(self) -> None:
        """Ensures a consistent ordering of generated features when `__iter__`
        is called.

        TODO: consider preventing this object from changing state at this point

        See `__iter__` for more details.
        """
        self._ordered_pool = list(sorted(self._pool, key=hash))

    def __iter__(self) -> Iterator[GeneratedFeatureNode]:
        """Returns the `GeneratedFeatureNode` Set as a sorted Iterable

        Sorting is done by hashing values or the name representation of
        the operation tree. Computing values is expensive, which is why
        we can't do this all the time, and resolving two identical expressions
        is also expensive which is why we rely on hashing values to ensure
        two generated features are distinct.

        This causes potential issues, since the ordering now depends on
        whether the values have been computed or not for a particular
        generated feature.

        To resolve this, if a consistently ordered Iterable is desired, one
        should call `lock` first, which will lock the order of the pool to be
        consistent each time this function is called UNTIL the pool is altered.
        """
        if self._ordered_pool:
            return iter(self._ordered_pool)
        return iter(sorted(self._pool, key=hash))

    def __len__(self) -> int:
        """Get number of features in the `pool`"""
        return len(self._pool)

    def get_features(self) -> List[GeneratedFeatureNode]:
        """Get features in the `pool` as a list (unsorted)"""
        return list(self._pool)

    def sample_features(self, batch_size: int, rng: np.random.Generator) -> List[GeneratedFeatureNode]:
        """Get a subset of the features in the `pool`

        Args:
            batch_size (int): the number of features to select
            rng (np.random.Generator): random generator for sampling features
        """
        assert batch_size <= len(self._pool)
        # @mypy: rng.choice is hard to deal with as it has a complex overload
        return rng.choice(list(self._pool), batch_size).tolist()  # type: ignore

    def to_df(self) -> pd.DataFrame:
        """Returns the generated features as a DataFrame"""
        assert all(gf.values is not None for gf in self._pool)
        return pd.DataFrame({gf.name: gf.values for gf in self._pool})

    # COMPARISONS

    def __contains__(self, item: GeneratedFeatureNode) -> bool:
        """Checks whether a feature has been cached."""
        assert isinstance(item, GeneratedFeatureNode)
        return hash(item) in self._cache

    def is_duplicate_name(self, feature: GeneratedFeatureNode) -> bool:
        """Checks whether a feature already exists based off its preordered
        representation.
        """
        return feature.preorder in self._names

    # ADD / REMOVE

    def clear(self) -> None:
        """Reset this object entirely."""
        self._cache.clear()
        self._names.clear()
        self._regenerate.clear()
        self._pool.clear()
        self._ordered_pool.clear()

    def clear_pool(self) -> None:
        """Reset the pool of generated features, but preserve the cache."""
        self._pool.clear()

    def regenerate_pool(self) -> None:
        """Add the `GeneratedFeatureNode` items from `_regenerate` to `_pool`"""
        self._pool.update(self._regenerate)

    def cache_generated_feature(self, feature: GeneratedFeatureNode) -> None:
        """Add a `GeneratedFeatureNode` to the cache without adding it to the
        `_pool`
        """
        self._cache.add(hash(feature))
        self._names.add(feature.preorder)

    def update_pool(self, other: FeatureGenerationPool) -> None:
        """Combine another `FeatureGenerationPool` into this one.

        Combines the caches, and replaces the contents of the `_pool` with
        the contents from the other `FeatureGenerationPool`.
        """
        self._pool = other._pool
        self._cache.update(other._cache)
        self._names.update(other._names)

    def spawn_new_pool(self) -> FeatureGenerationPool:
        """Similar to a copy, however the new `FeatureGenerationPool`
        has an empty `_regenerate` and `_pool` and only keeps the cache.
        """
        new_pool = FeatureGenerationPool()
        new_pool._cache = self._cache.copy()
        new_pool._names = self._names.copy()
        return new_pool

    def remove_names(self, features: List[str]) -> None:
        """Remove a list of features from the `_pool` by name.

        Args:
            features (List[str]): the list of features to remove.
        """
        pool = self._pool.copy()
        for feature in pool:
            if feature.name in features:
                self._pool.remove(feature)

    # UTILITY

    def get_feature_lengths(self) -> Dict[str, int]:
        """Get the length of each feature (the number of nodes in the expression
        tree).

        Return:
            Dict[str, int]: keys are the names of the features, values are the
                lengths of the expression tree of each feature.
        """
        return {gf.name: len(gf) for gf in self._pool}

    def homogeneity(self) -> float:
        """A metric of how correlated the generated features are.

        Return:
            float: a value between 0.0 and 1.0. 0.0 implies the generated
                features are maximally different, 1.0 implies the generated
                features are perfectly correlated, and most likely identical.
        """
        corr = 0.0
        i = 0
        for pair in itertools.combinations(self._pool, 2):
            if pair[0].values is None or pair[1].values is None:
                continue
            if hash(pair[0]) > hash(pair[1]):
                corr += abs(pair[0].values.corr(pair[1].values))
                i += 1
        return corr / i if i > 0 else corr
