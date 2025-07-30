from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import PrimitiveType

from .asset import Asset
from .space import AssetSpace

class Additive(Asset):
    """AdditiveAsset represents a numeric asset where the aggregation is additive."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        init_fn_or_value: PrimitiveType | AssetSpace | Callable[[], Any] | None = None,
        functional: bool = True,
    ) -> None:
        """Create a new Additive asset.

        Args:
            lower_bound (float): The lower bound of the asset.
            upper_bound (float): The upper bound of the asset.
            init_fn_or_value (Optional[Union[PrimitiveType, AssetSpace, Callable[[], Any]]]):
                The function to initialize the asset. It can be a primitive type, a
                callable with no arguments or an `AssetSpace` object. If it is not
                provided, the asset will be initialized with the lower bound.
                Defaults to None.
            functional (bool, optional): If True, the asset is functional. Defaults to
                True.

        Raises:
            ValueError: If $lower_bound > upper_bound$.
        """

    def aggregate(self, *assets: float) -> float:
        """Aggregate the assets into a single asset via summation.

        Args:
            assets (Iterable[float]): The assets to aggregate.

        Returns:
            float: The aggregated asset.
        """

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check asset1 contains asset2. In an additive asset, the higher value contains
        the lower value.

        Args:
            asset1 (float): The "container" asset.
            asset2 (float): The "contained" asset.

        Returns:
            True if asset1 >= asset2, False otherwise.
        """

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (float): The asset to be checked.

        Returns:
            True if lower_bound <= asset <= upper_bound, False otherwise.
        """
