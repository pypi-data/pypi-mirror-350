"""A VehicleCluster defines a set of vehicles of a specific make and model.

Vehicle clusters are shown in the showroom of the web app.
"""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, Field

from athlon_flex_client.models.vehicle import Vehicle  # noqa: TCH001


class VehicleCluster(BaseModel):
    """Vehicle Cluster model.

    A Cluster defines a vehicle make and type. All registered
    cars belong to the cluster of its make and type.
    """

    firstVehicleId: str
    externalTypeId: str
    make: str
    model: str
    latestModelYear: int
    vehicleCount: int
    minPriceInEuroPerMonth: float
    fiscalValueInEuro: float
    additionPercentage: float | None = None
    externalFuelTypeId: int
    maxCO2Emission: int
    imageUri: str

    vehicles: list[Vehicle] | None = Field(init=False, optional=True, default=None)

    def __str__(self) -> str:
        """Return the string representation of the vehicle cluster.

        Shows the make and model, and all vehicles in the cluster (if loaded).
        """
        msg = f"{self.make} {self.model}"
        if self.vehicles:
            msg = (
                msg + "\n" + "\n".join("\t" + str(vehicle) for vehicle in self.vehicles)
            )
        return msg


class VehicleClusters(BaseModel):
    """Collection of vehicle clusters."""

    vehicle_clusters: list[VehicleCluster]

    def __str__(self) -> str:
        """Return the string representation of the vehicle clusters.

        Show one cluster per line.
        """
        header = "Vehicle Clusters:"
        separator = "\n" + "-" * len(header) + "\n"
        vehicles = "\n".join(str(vehicle) for vehicle in self.vehicle_clusters)
        return f"{header}{separator}{vehicles}"

    def __iter__(self) -> iter[VehicleCluster]:
        """Iterate over the vehicle clusters."""
        return iter(self.vehicle_clusters)

    def __getitem__(self, index: int) -> VehicleCluster:
        """Get the vehicle cluster at the given index."""
        return self.vehicle_clusters[index]


class DetailLevel(IntEnum):
    """The level of detail to include in a VehicleCluster object.

    More detail means more requests. Used in the API Client to determine
    what to load.

    Attributes:
        CLUSTER_ONLY: Only include the cluster details, do not load the vehicles.
            Requires one request.
        INCLUDE_VEHICLES: Also load the vehicles of the cluster.
            Requires one request per cluster.
        INCLUDE_VEHICLE_DETAILS: Include extra details of the vehicles.
            Requires one request per vehicle.

    """

    CLUSTER_ONLY = 0
    INCLUDE_VEHICLES = 1
    INCLUDE_VEHICLE_DETAILS = 2
