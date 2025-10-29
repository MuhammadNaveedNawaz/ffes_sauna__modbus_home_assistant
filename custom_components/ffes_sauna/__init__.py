"""The FFES Sauna integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import voluptuous as vol

from .const import (
    ATTR_DURATION,
    ATTR_HUMIDITY,
    ATTR_PROFILE,
    ATTR_TEMPERATURE,
    CONF_SLAVE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PROFILE_DRY_SAUNA,
    REG_CONTROLLER_STATUS,
    REG_SAUNA_PROFILE,
    REG_SESSION_TIME,
    REG_TEMPERATURE_SET,
    REG_VAPORIZER_HUMIDITY,
    SAUNA_PROFILES,
    SERVICE_SET_PROFILE,
    SERVICE_START_SESSION,
    SERVICE_STOP_SESSION,
    STATUS_HEAT,
    STATUS_OFF,
)
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up FFES Sauna from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    slave = entry.data[CONF_SLAVE]
    name = entry.data[CONF_NAME]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = FFESSaunaCoordinator(
        hass=hass,
        host=host,
        port=port,
        slave=slave,
        name=name,
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def handle_start_session(call: ServiceCall) -> None:
        """Handle the start_session service call."""
        profile = call.data.get(ATTR_PROFILE, PROFILE_DRY_SAUNA)
        temperature = call.data.get(ATTR_TEMPERATURE, 85)
        duration = call.data.get(ATTR_DURATION, 60)
        humidity = call.data.get(ATTR_HUMIDITY)

        try:
            # Set profile
            await coordinator.write_register(REG_SAUNA_PROFILE, profile)
            
            # Set temperature
            await coordinator.write_register(REG_TEMPERATURE_SET, temperature)
            
            # Set duration
            await coordinator.write_register(REG_SESSION_TIME, duration)
            
            # Set humidity if provided (for wet sauna)
            if humidity is not None:
                await coordinator.write_register(REG_VAPORIZER_HUMIDITY, humidity)
            
            # Start session
            await coordinator.write_register(REG_CONTROLLER_STATUS, STATUS_HEAT)
            
            await coordinator.async_request_refresh()
            
            _LOGGER.info(
                "Started sauna session: profile=%s, temp=%s, duration=%s",
                profile,
                temperature,
                duration,
            )
        except Exception as err:
            _LOGGER.error("Error starting sauna session: %s", err)
            raise

    async def handle_stop_session(call: ServiceCall) -> None:
        """Handle the stop_session service call."""
        try:
            await coordinator.write_register(REG_CONTROLLER_STATUS, STATUS_OFF)
            await coordinator.async_request_refresh()
            _LOGGER.info("Stopped sauna session")
        except Exception as err:
            _LOGGER.error("Error stopping sauna session: %s", err)
            raise

    async def handle_set_profile(call: ServiceCall) -> None:
        """Handle the set_profile service call."""
        profile_name = call.data.get(ATTR_PROFILE)
        
        # Convert profile name to number
        profile_num = next(
            (k for k, v in SAUNA_PROFILES.items() if v == profile_name),
            None
        )
        
        if profile_num is None:
            _LOGGER.error("Invalid profile name: %s", profile_name)
            return
        
        try:
            # Can only change profile when controller is off or standby
            current_status = coordinator.data.get("controller_status", STATUS_OFF)
            if current_status not in [STATUS_OFF, 3]:  # 3 = STATUS_STBY
                _LOGGER.warning(
                    "Cannot change profile while sauna is active. Stop session first."
                )
                return
            
            await coordinator.write_register(REG_SAUNA_PROFILE, profile_num)
            await coordinator.async_request_refresh()
            
            _LOGGER.info("Changed sauna profile to: %s", profile_name)
        except Exception as err:
            _LOGGER.error("Error changing sauna profile: %s", err)
            raise

    # Service schemas
    start_session_schema = vol.Schema(
        {
            vol.Required(ATTR_PROFILE, default=PROFILE_DRY_SAUNA): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=7)
            ),
            vol.Required(ATTR_TEMPERATURE, default=85): vol.All(
                vol.Coerce(int), vol.Range(min=20, max=110)
            ),
            vol.Required(ATTR_DURATION, default=60): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=2000)
            ),
            vol.Optional(ATTR_HUMIDITY): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
        }
    )

    stop_session_schema = vol.Schema({})

    set_profile_schema = vol.Schema(
        {
            vol.Required(ATTR_PROFILE): vol.In(list(SAUNA_PROFILES.values())),
        }
    )

    hass.services.async_register(
        DOMAIN, SERVICE_START_SESSION, handle_start_session, schema=start_session_schema
    )
    hass.services.async_register(
        DOMAIN, SERVICE_STOP_SESSION, handle_stop_session, schema=stop_session_schema
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SET_PROFILE, handle_set_profile, schema=set_profile_schema
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

    # Unregister services if this was the last entry
    if not hass.data[DOMAIN]:
        hass.services.async_remove(DOMAIN, SERVICE_START_SESSION)
        hass.services.async_remove(DOMAIN, SERVICE_STOP_SESSION)
        hass.services.async_remove(DOMAIN, SERVICE_SET_PROFILE)

    return unload_ok
