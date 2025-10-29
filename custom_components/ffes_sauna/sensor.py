"""Sensor platform for FFES Sauna."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class FFESSaunaSensorDescription(SensorEntityDescription):
    """Class describing FFES Sauna sensor entities."""

    value_fn: Callable[[dict], StateType] | None = None


SENSORS: tuple[FFESSaunaSensorDescription, ...] = (
    FFESSaunaSensorDescription(
        key="temperature_actual",
        name="Current Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("temperature_actual"),
    ),
    FFESSaunaSensorDescription(
        key="temperature_set",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("temperature_set"),
    ),
    FFESSaunaSensorDescription(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("humidity_actual"),
    ),
    FFESSaunaSensorDescription(
        key="session_time",
        name="Session Time",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        value_fn=lambda data: data.get("session_time"),
    ),
    FFESSaunaSensorDescription(
        key="ventilation_time",
        name="Ventilation Time",
        icon="mdi:fan",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        value_fn=lambda data: data.get("ventilation_time"),
    ),
    FFESSaunaSensorDescription(
        key="status",
        name="Status",
        icon="mdi:information",
        value_fn=lambda data: data.get("controller_status_name"),
    ),
    FFESSaunaSensorDescription(
        key="profile",
        name="Profile",
        icon="mdi:fire",
        value_fn=lambda data: data.get("profile"),
    ),
    FFESSaunaSensorDescription(
        key="error_code",
        name="Error Code",
        icon="mdi:alert-circle",
        value_fn=lambda data: data.get("error_code"),
    ),
    FFESSaunaSensorDescription(
        key="error_message",
        name="Error Message",
        icon="mdi:message-alert",
        value_fn=lambda data: data.get("error_message"),
    ),
    FFESSaunaSensorDescription(
        key="aromatherapy",
        name="Aromatherapy",
        icon="mdi:flower",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("aromatherapy"),
    ),
    FFESSaunaSensorDescription(
        key="software_version",
        name="Software Version",
        icon="mdi:information",
        value_fn=lambda data: data.get("software_version"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna sensors from a config entry."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities(
        FFESSaunaSensor(coordinator, entry, description)
        for description in SENSORS
    )


class FFESSaunaSensor(CoordinatorEntity[FFESSaunaCoordinator], SensorEntity):
    """Representation of a FFES Sauna sensor."""

    entity_description: FFESSaunaSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        entry: ConfigEntry,
        description: FFESSaunaSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data["name"],
            "manufacturer": "FFES",
            "model": "Sauna Controller",
        }

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None
