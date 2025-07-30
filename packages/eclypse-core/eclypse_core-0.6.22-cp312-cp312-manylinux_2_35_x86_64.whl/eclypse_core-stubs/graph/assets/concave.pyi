from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import PrimitiveType

from .asset import Asset
from .space import AssetSpace

class Concave(Asset):
    """ConcaveAsset represents a numeric asset where the aggregation is concave."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        init_fn_or_value: PrimitiveType | AssetSpace | Callable[[], Any] | None = None,
        functional: bool = True,
    ) -> None:
        """Create a new Concave asset.

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

    def aggregate(self, *assets) -> float:
        """Aggregate the assets into a single asset by taking the maximum value. If no
        assets are provided, the lower bound is returned.

        Args:
            assets (Iterable[TConcave]): The assets to aggregate.

        Returns:
            TConcave: The aggregated asset.
        """

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check if asset1 contains asset2. In the ordering of a concave asset, the
        lower value contains the other.

        Args:
            asset1 (TConcave): The "container" asset.
            asset2 (TConcave): The "contained" asset.

        Returns:
            bool: True if asset1 <= asset2, False otherwise.
        """

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound]."""

    def flip(self): ...
