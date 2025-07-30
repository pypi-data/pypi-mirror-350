"""Used to filter what VehicleClusters should be loaded from the API.

In most cases, this filter is created based on the user's profile settings. This results
in the same set of Vehicles that is shown in the web app.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from athlon_flex_client.models.filters.filter import Filter

if TYPE_CHECKING:
    from athlon_flex_client.models.profile import Profile


class VehicleClusterFilter(Filter):
    """Filters for loading the Vehicle Clusters."""

    Segment: str | None = "Cars"
    IncludeTaxInPrices: bool | None = None
    NumberOfKmPerMonth: int | None = None
    IncludeMileageCostsInPricing: bool | None = None
    IncludeFuelCostsInPricing: bool | None = None

    @staticmethod
    def from_profile(profile: Profile) -> VehicleClusterFilter:
        """Create a filter from a profile."""
        return VehicleClusterFilter(
            IncludeTaxInPrices=profile.requiresIncludeTaxInPrices,
            NumberOfKmPerMonth=profile.numberOfKmPerMonth,
            IncludeMileageCostsInPricing=profile.includeMileageCostsInPricing,
            IncludeFuelCostsInPricing=profile.includeFuelCostsInPricing,
        )


class AllVehicleClusters(VehicleClusterFilter):
    """Empty filter for loading all items.

    Using this filter would load all available VehicleClusters, irregarding
    of whether the user can lease them. This is equivalent to opening the showroom
    web app without being logged in.
    """
