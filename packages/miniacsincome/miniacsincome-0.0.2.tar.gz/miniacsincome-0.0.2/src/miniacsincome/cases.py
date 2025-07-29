# Copyright (c) 2025 David Boetius
# Licensed under the MIT license
from typing import Union
from pathlib import Path
import os

import dill
import torch
from torch import nn
from torchstats import BayesianNetwork, TabularInputSpace
from huggingface_hub import hf_hub_download


__all__ = ["get_population_model", "get_network"]


def get_population_model(
    num_variables: int,
    root: Union[str, os.PathLike] = ".datasets",
    download: bool = False,
) -> tuple[BayesianNetwork, TabularInputSpace, nn.Module]:
    """Loads a population model, input space, and input transformation for MiniACSIncome.

    :param num_variables: The number of input variables in the `MiniACSIncome` dataset.
    :param root: The root directory containing the data.
    :param download: Whether to download the population model if it is not present in the
        `root` directory.
    :return: A tuple of (input distribution, input space, population model transformation).
    """
    root = Path(root) / "MiniACSIncome"
    filename = f"bayes_net_{num_variables}_var_population_model.pyt"

    if download:
        hf_hub_download(
            repo_id="davidboetius/MiniACSIncome",
            filename=filename,
            repo_type="model",
            local_dir=root,
        )
    return torch.load(root / filename, pickle_module=dill)


def get_network(
    num_variables: int,
    depth: int | None = None,
    size: int | None = None,
    root: Union[str, os.PathLike] = ".datasets",
    download: bool = False,
) -> nn.Sequential:
    """Loads a MiniACSIncome network.

    The following combinations are available:
     - num_variables=1, depth=None, size=None
     - num_variables=2, depth=None, size=None
     - num_variables=3, depth=None, size=None
     - num_variables=4, depth=None, size=None
     - num_variables=5, depth=None, size=None
     - num_variables=6, depth=None, size=None
     - num_variables=7, depth=None, size=None
     - num_variables=8, depth=None, size=None
     - num_variables=4, depth=2, size=None
     - num_variables=4, depth=3, size=None
     - num_variables=4, depth=4, size=None
     - num_variables=4, depth=5, size=None
     - num_variables=4, depth=6, size=None
     - num_variables=4, depth=7, size=None
     - num_variables=4, depth=8, size=None
     - num_variables=4, depth=9, size=None
     - num_variables=4, depth=10, size=None
     - num_variables=4, depth=None, size=1000
     - num_variables=4, depth=None, size=2000
     - num_variables=4, depth=None, size=3000
     - num_variables=4, depth=None, size=4000
     - num_variables=4, depth=None, size=5000
     - num_variables=4, depth=None, size=6000
     - num_variables=4, depth=None, size=7000
     - num_variables=4, depth=None, size=8000
     - num_variables=4, depth=None, size=9000
     - num_variables=4, depth=None, size=10000

    :param num_variables: The number of input variables in the `MiniACSIncome` dataset.
    :param depth: The depth of the network.
    :param size: The number of neurons in the hidden layer.
    :param root: The root directory containing the data.
    :param download: Whether to download the population model if it is not present in the
        `root` directory.
    :return: A neural network.
    """
    if depth is None and size is None:
        net_name = "network"
    elif depth is not None and size is None:
        net_name = f"depth_{depth}"
    elif depth is None and size is not None:
        net_name = f"size_{size}"
    else:
        raise ValueError("Can not load network: Either depth or size must be None.")

    root = Path(root) / "MiniACSIncome"
    filename = f"MiniACSIncome-{num_variables}_{net_name}.pyt"
    if download:
        hf_hub_download(
            repo_id="davidboetius/MiniACSIncome",
            filename=filename,
            repo_type="model",
            local_dir=root,
        )
    return torch.load(root / filename, weights_only=False)
