"""A VehicleFilter is used to filter what Vehicles should be loaded from the API.

In most cases, this filter is created based on the user's profile settings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from athlon_flex_client.models.filters.filter import Filter

if TYPE_CHECKING:
    from athlon_flex_client.models.profile import Profile


class VehicleFilter(Filter):
    """Filters for loading the Vehicle Clusters.

    Attributes:
        VehicleId: str | None
            Only used if the filter is used to load vehicle details.

    """

    Segment: str = "Cars"
    VehicleId: str | None = None
    Make: str | None = None
    Model: str | None = None
    IncludeTaxInPrices: bool | None = None
    NumberOfKmPerMonth: int | None = None
    IncludeMileageCostsInPricing: bool | None = None
    IncludeFuelCostsInPricing: bool | None = None
    SortBy: str = "PriceInEuro"
    MaxPricePerMonth: int | float | None = None
    ActualBudgetPerMonth: int | float | None = None

    @staticmethod
    def from_profile(make: str, model: str, profile: Profile) -> VehicleFilter:
        """Create a filter from a profile."""
        return VehicleFilter(
            Make=make,
            Model=model,
            IncludeTaxInPrices=profile.requiresIncludeTaxInPrices,
            NumberOfKmPerMonth=profile.numberOfKmPerMonth,
            IncludeMileageCostsInPricing=profile.includeMileageCostsInPricing,
            IncludeFuelCostsInPricing=profile.includeFuelCostsInPricing,
            MaxPricePerMonth=profile.budget.maxBudgetPerMonth,
            ActualBudgetPerMonth=profile.budget.actualBudgetPerMonth,
        )
