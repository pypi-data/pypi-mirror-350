from __future__ import annotations

from typing import Self, TypeVar, override

import numpy as np
from jax import tree

from .annotations import JaxArray, NumpyRealArray

T = TypeVar('T')


class Projectable:
    """Base class to override how an element of a PyTree is projected."""
    def project(self, projector: Projector) -> Self:
        raise NotImplementedError


class Projector:
    """A tool to project the arrays in a PyTree to fewer dimensions. This is useful for graphing."""
    @override
    def __init__(self, *, seed: int = 0, dimensions: int = 2) -> None:
        super().__init__()
        self.seed = seed
        self.dimensions = dimensions
        self.projection_matrices: dict[int, NumpyRealArray] = {}

    def project_tree(self, projectable: T) -> T:
        """Project the arrays in a PyTree to the plane."""
        return tree.map(self.project, projectable, is_leaf=lambda x: isinstance(x, Projectable))

    def project(self, projectable: T) -> T:
        """Project an array or Projectable instance to the plane."""
        if projectable is None:
            return projectable
        if isinstance(projectable, Projectable):
            return projectable.project(self)

        assert isinstance(projectable, (JaxArray, np.ndarray))
        features = projectable.shape[-1]
        if features <= self.dimensions:
            return projectable
        projection_matrix = self.get_projection_matrix(features)
        return projectable @ projection_matrix  # type: ignore[return-value] # pyright: ignore

    def get_projection_matrix(self, features: int) -> NumpyRealArray:
        if features not in self.projection_matrices:
            self.projection_matrices[features] = _random_directions(self.seed, features,
                                                                    self.dimensions)
        return self.projection_matrices[features]


def _random_directions(seed: int, dimensions: int, n_axes: int) -> NumpyRealArray:
    """Produce a random projection matrix.

    Returns: a matrix of random numbers with `n_axes` columns, of length `dimensions`, each of
    which is mutually orthogonal and unit-length.
    """
    if dimensions < n_axes:
        raise ValueError
    if seed == 0 and dimensions == n_axes:
        return np.eye(dimensions)
    np_rng = np.random.default_rng(seed)
    a = np_rng.uniform(size=(dimensions, n_axes))
    directions, _ = np.linalg.qr(a, mode='reduced')
    assert isinstance(directions, np.ndarray)
    return directions
