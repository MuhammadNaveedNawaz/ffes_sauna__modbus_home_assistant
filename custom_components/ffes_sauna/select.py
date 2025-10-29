"""Select platform for FFES Sauna."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    PROFILE_NAMES,
    REG_SAUNA_PROFILE,
    SAUNA_PROFILES,
)
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna select from a config entry."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([FFESSaunaProfileSelect(coordinator, entry)])


class FFESSaunaProfileSelect(CoordinatorEntity[FFESSaunaCoordinator], SelectEntity):
    """Representation of a FFES Sauna profile selector."""

    _attr_has_entity_name = True
    _attr_name = "Profile"
    _attr_icon = "mdi:format-list-bulleted"

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_profile_select"
        self._attr_options = list(PROFILE_NAMES.values())
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data["name"],
            "manufacturer": "FFES",
            "model": "Sauna Controller",
        }

    @property
    def current_option(self) -> str | None:
        """Return the current selected profile."""
        profile = self.coordinator.data.get("profile")
        if profile:
            return PROFILE_NAMES.get(profile)
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected profile."""
        # Find the profile number for the selected name
        profile_num = next(
            (k for k, v in SAUNA_PROFILES.items() if PROFILE_NAMES.get(v) == option),
            None,
        )
        
        if profile_num is None:
            _LOGGER.error("Invalid profile option: %s", option)
            return
        
        try:
            await self.coordinator.write_register(REG_SAUNA_PROFILE, profile_num)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error setting profile: %s", err)
            raise
