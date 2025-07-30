from typing import Any

from .asset import Asset

class AssetBucket(dict[str, Asset]):
    """Class to store a set of nodes/services assets."""

    def __init__(self, **assets) -> None:
        """Create a new asset bucket.

        Args:
            **assets (Dict[str, Asset]): The assets to store in the bucket.
        """

    def __setitem__(self, key: str, value: Asset) -> None:
        """Set an asset in the bucket.

        Args:
            key (str): The key of the asset.
            value (Asset): The asset to store.
        """

    def aggregate(self, *assets: dict[str, Any]) -> dict[str, Any]:
        """Aggregate the assets into a single asset.

        Args:
            assets (Iterable[Dict[str, Any]]): The assets to aggregate.

        Returns:
            Dict[str, Any]: The aggregated asset.
        """

    def satisfies(
        self,
        assets: dict[str, Any],
        constraints: dict[str, Any],
        violations: bool = False,
    ) -> bool | dict[str, dict[str, Any]]:
        """Checks whether the given asset satisfies the provided constraints.

            Only functional assets that exist in both buckets are considered.
            If any key fails its individual `satisfies` check, it is treated as a violation.

            Args:
                assets (Dict[str, Any]): The dictionary of asset values to evaluate.
                constraints (Dict[str, Any]): The constraint values to satisfy.
                violations (bool, optional): If True, return a dictionary containing
                    only the violated keys and their asset/constraint values.
                    If False (default), return a boolean indicating overall satisfaction.

            Returns:
                Union[bool, Dict[str, Dict[str, Any]]]:
                    - If `violations=False`: True if all constraints are satisfied,
        False otherwise.
                    - If `violations=True`: A dictionary of violations,
        empty if all constraints pass.
        """

    def consume(
        self, assets: dict[str, Any], amounts: dict[str, Any]
    ) -> dict[str, Any]:
        """Consume the `amount` of the asset from the `asset`.

        Args:
            assets (Dict[str, Any]): The asset to consume from.
            amounts (Dict[str, Any]): The amount to consume.

        Returns:
            Dict[str, Any]: The remaining assets after the consumption.
        """

    def is_consistent(
        self, assets: dict[str, Any], violations: bool = False
    ) -> bool | dict[str, Any]:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

            Args:
                asset (Dict[str, Any]): The asset to be checked.
                violations (bool, optional): If True, return a dictionary containing
                    only the violated keys and their asset/constraint values.
                    If False (default), return a boolean indicating overall satisfaction.

            Returns:
                Union[bool, Dict[str, Any]]:
                    - If `violations=False`: True if all constraints are satisfied,
        False otherwise.
                    - If `violations=True`: A dictionary of violations,
        empty if all assets are consistent.
        """

    def flip(self):
        """Flip the assets of the bucket, thus moving from node capabilities to service
        requirements.

        Returns:
            AssetBucket: The flipped asset bucket.
        """

    @property
    def lower_bound(self) -> dict[str, Any]:
        """Return the lower bound of the asset bucket, i.e. the lower bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The lower bound of the asset bucket.
        """

    @property
    def upper_bound(self) -> dict[str, Any]:
        """Return the upper bound of the asset bucket, i.e. the upper bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The upper bound of the asset bucket.
        """
