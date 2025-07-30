"""The TaxRate model is used by Athlon to compute the net costs of a vehicle."""

from __future__ import annotations

import re

from pydantic import BaseModel

from athlon_flex_client import logger


class TaxRate(BaseModel):
    """Tax rate model.

    Athlon uses tax rates to compote the (estimate) net costs of a vehicle.
    The API client optionally consumes the (approximate) gross yearly income
    of the user, and then uses it to select the correct tax rate. The tax rate
    is stored in the cookies, and the API will then include the net prices
    in its response.

    Attributes:
        label: str The label of the tax rate.
            Used to extract the following information about the tax rate:
            - Whether loonheffingskorting is applied or not.
            - The lower and upper bounds of the tax rate.
            Extraction is done using regex.
            Example label:
                "Met loonheffingskorting jaarinkomen € 75.519 t/m € 134.929"
        percentage: float The percentage of the tax rate.

    """

    label: str
    percentage: float

    @property
    def bounds(self) -> tuple[float, float]:
        """Return the lower and upper bounds of the tax rate.

        If a single value v is found, return (v, inf)
        If no values are found, both bounds are set to 0.0
            an income will never match this rate.
        """
        pattern = r"€\s?(\d+(?:\.\d+)?)"
        matches = re.findall(pattern, self.label)
        matches = [match.replace(".", "") for match in matches]
        if matches and 0 < len(matches) <= 2:  # noqa: PLR2004
            if len(matches) == 1:
                lower_bound = matches[0]
                return float(lower_bound), float("inf")
            lower_bound, upper_bound = matches
            return float(lower_bound), float(upper_bound)
        return 0.0, 0.0

    def is_for_income(self, income: float, *, apply_loonheffingskorting: bool) -> bool:
        """Check if the tax rate is for the given income.

        Args:
            income (float): Check whether this income is within the bounds of the rate.
            apply_loonheffingskorting (bool): Check whether the label indicates
                loonheffingskorting or not

        Returns:
                bool: Whether the tax rate is for the given income.

        """
        lower_bound, upper_bound = self.bounds
        income_match = lower_bound <= income <= upper_bound
        str_to_find = (
            "Met" if apply_loonheffingskorting else "Zonder"
        ) + " loonheffingskorting"
        loonheffingskorting_match = str_to_find in self.label
        return income_match and loonheffingskorting_match


class TaxRates(BaseModel):
    """Collection of tax rates."""

    tax_rates: list[TaxRate]

    def rate_of_income(
        self,
        gross_yearly_income: float | None,
        *,
        apply_loonheffingskorting: bool,
    ) -> TaxRate | None:
        """Return the tax rate for the given income.

        Args:
            gross_yearly_income (float): The income to get the tax rate for.
            apply_loonheffingskorting (bool): Whether to apply the loonheffingskorting.

        Returns:
            TaxRate | None: The tax rate for the given income.
            None if no or multiple rates are found.

        """
        if not gross_yearly_income:
            return None
        rates = [
            rate
            for rate in self.tax_rates
            if rate.is_for_income(
                gross_yearly_income,
                apply_loonheffingskorting=apply_loonheffingskorting,
            )
        ]
        if len(rates) == 1:
            return rates[0]
        logger.warning(f"Found {len(rates)} rates for income: {gross_yearly_income}")
        return None
