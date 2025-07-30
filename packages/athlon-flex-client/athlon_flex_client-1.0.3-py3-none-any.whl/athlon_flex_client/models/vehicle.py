"""A Vehicle represents a specific instance of a vehicle in a VehicleCluster.

Vehicles are shown in the web app when a VehicleCluster is selected.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from athlon_flex_client.models.filters.filter import Filter

if TYPE_CHECKING:
    from athlon_flex_client.models.profile import Profile


class Vehicle(BaseModel):
    """Vehicle model.

    A Vehicle defines a specific vehicle configuration.
    For example one instance of the Opel Corsa E. It belongs to the VehicleCluster
    of its make and type.

    The class has a structure as defined by the API. Some details are optional,
    and only loaded when requested by the user (see DetailLevel).
    """

    class Details(BaseModel):
        """Vehicle details."""

        licensePlate: str
        color: str
        officialColor: str
        bodyType: str
        emission: float
        registrationDate: str
        registeredMileage: float
        transmissionType: str
        avgFuelConsumption: float
        typeSpareWheel: str
        additionPercentage: float | None = None

    class Pricing(BaseModel):
        """Vehicle pricing.

        Attributes:
            netCostPerMonthInEuro: float | None = None
                Only if the tax rate cookies are set.
                    See AthlonFlexClient._set_tax_rate_cookie

        """

        fiscalValueInEuro: float
        basePricePerMonthInEuro: float
        calculatedPricePerMonthInEuro: float
        pricePerKm: float
        fuelPricePerKm: float
        contributionInEuro: float | None = None
        expectedFuelCostPerMonthInEuro: float
        netCostPerMonthInEuro: float | None = None

    class Option(BaseModel):
        """Vehicle option.

        Example: Trekhaak.
        """

        id: str
        externalId: str
        optionName: str
        included: bool

    id: str
    make: str
    model: str
    type: str
    modelYear: int
    paintId: str | None = None
    externalPaintId: str | None = None
    priceInEuroPerMonth: float | None = None
    fiscalValueInEuro: float | None = None
    additionPercentage: float | None = None
    rangeInKm: int
    externalFuelTypeId: int
    externalTypeId: str
    imageUri: str | None = None
    isElectric: bool | None = None
    details: Details | None = None
    pricing: Pricing | None = None
    options: list[Option] | None = None

    def __str__(self) -> str:
        """Return the string representation of the vehicle.

        Includes the make, model, type, and model year.
        """
        return f"{self.make} {self.model} {self.type} {self.modelYear}"

    def details_request_params_from_profile(
        self,
        profile: Profile,
    ) -> dict[str, str | int]:
        """Return the request parameters for loading the details of the vehicle.

        Used when logged in
        """
        bool_to_str = Filter.bool_to_str
        return {
            "Segment": "Cars",
            "VehicleId": self.id,
            "IncludeTaxInPrices": bool_to_str(profile.requiresIncludeTaxInPrices),
            "NumberOfKmPerMonth": profile.numberOfKmPerMonth,
            "IncludeMileageCostsInPricing": bool_to_str(
                profile.includeMileageCostsInPricing,
            ),
            "IncludeFuelCostsInPricing": bool_to_str(profile.includeFuelCostsInPricing),
            "ActualBudgetPerMonth": profile.budget.actualBudgetPerMonth,
        }

    def details_request_params_without_profile(self) -> dict[str, str | int]:
        """Return the request parameters for loading the details of the vehicle.

        Used when not logged in.
        """
        return {
            "Segment": "Cars",
            "VehicleId": self.id,
        }

    @property
    def uri(self) -> str:
        """The URI of the vehicle, to open the vehicle in the web app."""
        return (
            f"https://flex.athlon.com/app/showroom/{self.make}/{self.model}/{self.id}"
        )
