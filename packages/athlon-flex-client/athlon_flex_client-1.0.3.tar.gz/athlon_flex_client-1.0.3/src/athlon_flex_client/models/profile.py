"""The Profile model shows information about the user."""

from __future__ import annotations

from pydantic import BaseModel


class Profile(BaseModel):
    """The profile model shows information about the user."""

    class RelationshipManager(BaseModel):
        """The relationship manager of the user.

        Usually indicates contact details of the employer of the user.
        """

        name: str
        email: str
        phone: str

    class Budget(BaseModel):
        """Indicates all budget information of the user."""

        actualBudgetPerMonth: int | float
        maxBudgetPerMonth: int | float
        normBudgetPerMonth: int | float
        normBudgetGasolinePerMonth: int | float
        normBudgetElectricPerMonth: int | float
        maxBudgetGasolinePerMonth: int | float
        maxBudgetElectricPerMonth: int | float
        normUndershootPercentage: int | float
        maxNormUndershootPercentage: int | float
        savedBudget: int | float
        savedBudgetPayoutAllowed: bool
        holidayCarRaiseAllowed: bool

    class Address(BaseModel):
        """The address of the user."""

        street: str
        houseNumber: str
        houseNumberAddendum: str
        zipCode: str
        city: str

    class CurrentReservation(BaseModel):
        """The current reservation of the user, if any."""

        externalId: str
        startedAtUtc: str
        vehicleId: str
        vehicleExternalId: str
        hasLicenseCardAvailable: bool

    id: str
    initials: str
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    customerName: str
    isConsumer: bool
    flexPlus: bool
    relationshipManager: RelationshipManager
    requiresIncludeTaxInPrices: bool
    includeMileageCostsInPricing: bool
    includeFuelCostsInPricing: bool
    onlyShowNetMonthCosts: bool
    numberOfKmPerMonth: int
    remainingSwaps: int
    budget: Budget
    hideIntroPopup: bool | None = None
    chargingStationRequest: bool | None = None
    pendingCancelation: bool | None = None
    pendingBikeCancelation: bool | None = None
    pendingBudgetPayout: bool | None = None
    pendingHolidayCarRaise: bool | None = None
    deliveryAddress: Address | None = None
    officialAddress: Address | None = None
    currentReservation: CurrentReservation | None = None
    firstReservationAllowedFromUtc: str
    firstDeliveryAllowedFromUtc: str
    canOrderBike: bool | None = None
    canMakeReservation: bool | None = None
    canMakeReservationFromUtc: str | None = None
    canMakePickup: bool | None = None
    canMakeBikeReservation: bool | None = None
    canMakeBikePickup: bool | None = None
    canMakeFirstReservation: bool | None = None
    canDecline: bool | None = None
    canDeclineBike: bool | None = None
