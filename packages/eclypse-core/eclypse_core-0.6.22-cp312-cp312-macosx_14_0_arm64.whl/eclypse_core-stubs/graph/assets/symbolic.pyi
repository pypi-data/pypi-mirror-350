from typing import Any

from .asset import Asset

class Symbolic(Asset):
    """SymbolicAsset represents an asset defined as a list of symbolic variables.

    The logic of the asset is defined in terms of a set of constraints.
    """

    def aggregate(self, *assets: Any) -> Any:
        """Aggregate the assets into a single asset via union.

        Args:
            assets (Iterable[SymbolicAsset]): The assets to aggregate.

        Returns:
            SymbolicAsset: The aggregated asset.
        """

    def satisfies(self, asset: Any, constraint: Any) -> bool:
        """Check if asset1 contains asset2. In a symbolic asset, asset1 contains asset2
        if all the variables in asset2 are present in asset1.

        Args:
            asset1 (SymbolicAsset): The "container" asset.
            asset2 (SymbolicAsset): The "contained" asset.

        Returns:
            bool: True if asset1 >= asset2, False otherwise.
        """

    def is_consistent(self, asset: Any) -> bool:
        """Checks if all the lower bound variables are present in the asset and all the
        variables in the asset are present in the upper bound.

        Args:
            asset (SymbolicAsset): The asset to be checked.

        Returns: True if lower_bound <= asset <= upper_bound, False otherwise.
        """
