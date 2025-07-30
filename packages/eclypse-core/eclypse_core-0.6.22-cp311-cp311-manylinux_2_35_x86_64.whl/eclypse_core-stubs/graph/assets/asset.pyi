import abc
from abc import abstractmethod
from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import PrimitiveType

from .space import AssetSpace

class Asset(metaclass=abc.ABCMeta):
    """Asset represents a resource of the infrastructure, such as CPU, GPU, RAM or
    Availability.

    It provides the inteface for the basic algebraic functions between assets.
    """

    def __init__(
        self,
        lower_bound: Any,
        upper_bound: Any,
        init_fn_or_value: PrimitiveType | AssetSpace | Callable[[], Any] | None = None,
        functional: bool = True,
    ) -> None:
        """Initialize the asset with the lower and upper bounds.

        The lower and the upper bounds represent the element which is always contained in
        and the element the always contains the asset, respectively. Thus, they must
        respect the total ordering of the asset.

        The `init_fn_or_value` parameter is the function to initialize the asset. It can
        be a primitive type, a callable with no arguments or an `AssetSpace` object.
        If it is not provided, the asset will be initialized with the lower bound.

        The `functional` parameter indicates if the asset is functional or not, thus if
        it must be checked during the validation of a placement or not.

        Args:
            lower_bound (Any): The lower bound of the asset.
            upper_bound (Any): The upper bound of the asset.
            init_fn_or_value (Optional[Union[PrimitiveType, AssetSpace, Callable[[], Any]]]):
                The function to initialize the asset. It can be a primitive type, a
                callable with no arguments or an `AssetSpace` object. If it is not
                provided, the asset will be initialized with the lower bound.
                Defaults to None.
            functional (bool, optional): If True, the asset is functional. Defaults to
                True.
        Raises:
            ValueError: If the lower bound is not contained in the upper bound.
            TypeError: If the init_fn is not a callable or an AssetSpace object.
        """

    @abstractmethod
    def aggregate(self, *assets) -> Any:
        """Aggregate the assets into a single asset.

        Args:
            assets (Any): The assets to aggregate.
        """

    @abstractmethod
    def satisfies(self, asset: Any, constraint: Any) -> bool:
        """Check if the asset satisfies the constraint.

        Args:
            asset (Any): The asset to check.
            constraint (Any): The constraint to check.

        Returns:
            bool: True if the asset satisfies the constraint, False otherwise.
        """

    @abstractmethod
    def is_consistent(self, asset: Any) -> bool:
        """Check if the asset has a feasible value."""

    def flip(self) -> Asset:
        """Flip the asset. Move the perspective from being a "capability" to be a
        "requirement" and vice versa. By default, the asset is left unchanged, thus the
        method returns a copy of the asset.

        Returns:
            Asset: The flipped asset.
        """
