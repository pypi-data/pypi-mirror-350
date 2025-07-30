from random import Random
from typing import Any

__all__ = ["AssetSpace", "Choice", "Uniform", "Sample"]

class AssetSpace:
    """Base class for asset spaces."""

    def __call__(self, random: Random):
        """Return a value from the asset space.

        Args:
            random (Random): The random number generator.

        Returns:
            Any: A value from the asset space.

        Raises:
            NotImplementedError: If the method is not implemented.
        """

class Choice(AssetSpace):
    """Class to represent a choice between a set of values."""

    def __init__(self, choices: list[Any]) -> None:
        """Create a new Choice asset space.

        Args:
            choices (List[Any]): The possible values to choose from.
        """

    def __call__(self, random: Random):
        """Return a value from the choices.

        Args:
            random (Random): The random number generator.

        Returns:
            Any: A value from the choices.
        """

class Uniform(AssetSpace):
    """Class to represent a uniform distribution of values."""

    def __init__(self, low: float, high: float) -> None:
        """Create a new Uniform asset space.

        Args:
            low (float): The lower bound of the distribution.
            high (float): The upper bound of the distribution.
        """

    def __call__(self, random: Random):
        """Return a value from the uniform distribution.

        Args:
            random (Random): The random number generator.

        Returns:
            float: A value from the uniform distribution.
        """

class IntUniform(AssetSpace):
    """Class to represent a uniform distribution of integer values."""

    def __init__(self, low: int, high: int, step: int = 1) -> None:
        """Create a new IntUniform asset space.

        Args:
            low (int): The lower bound of the distribution.
            high (int): The upper bound of the distribution.
            step (int): The step size for the distribution.
                Default is 1.
        """

    def __call__(self, random: Random):
        """Return a value from the uniform distribution.

        Args:
            random (Random): The random number generator.

        Returns:
            int: A value from the uniform distribution.
        """

class Sample(AssetSpace):
    """Class to represent a sample of values from a population."""

    def __init__(
        self,
        population: list[Any],
        k: int | tuple[int, int],
        counts: list[int] | None = None,
    ) -> None:
        """Create a new Sample asset space. The sample is drawn from the population. The
        parameter `k` can be either an integer or a pair of integers representing the
        range from which to draw the sample size.

        Args:
            population (List[Any]): The population to sample from.
            k (Union[int, Tuple[int, int]]): The number of values to sample.
            counts (Optional[List[int]]): The counts for each element in the population.
        """

    def __call__(self, random: Random):
        """Return a sample of values from the population.

        Args:
            random (Random): The random number generator.

        Returns:
            List[Any]: A sample of values from the population.
        """
