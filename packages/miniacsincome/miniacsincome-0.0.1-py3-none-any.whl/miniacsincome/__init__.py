# Copyright (c) 2025 David Boetius
# Licensed under the MIT license
"""MiniACSIncome: A benchmark for fairness verification of neural networks."""

__version__ = "0.0.1"

from .miniacsincome import MiniACSIncome
from .cases import get_population_model, get_network

def download_all(root=".datasets"):
    MiniACSIncome(root=root, download=True)

    for n in range(1, 9):
        get_network(n, root=root, download=True)
        get_population_model(4, root=root, download=True)

    for depth in range(2, 11):
        get_network(4, depth=depth, root=root, download=True)

    for size in range(1000, 11000, 1000):
        get_network(4, size=size, root=root, download=True)


__all__ = ["MiniACSIncome", "get_population_model", "get_network", "download_all"]
