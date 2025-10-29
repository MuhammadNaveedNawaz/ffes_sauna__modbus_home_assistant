"""DataUpdateCoordinator for FFES Sauna."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    ERROR_CODES,
    REG_AROMA_SET_VALUE,
    REG_CONTROLLER_MODEL,
    REG_CONTROLLER_STATUS,
    REG_CPIR_G1_POWER,
    REG_CPIR_G2_POWER,
    REG_CPIR_G3_POWER,
    REG_CPIR_G4_POWER,
    REG_CPIR_GROUP_1_SET,
    REG_CPIR_GROUP_2_SET,
    REG_ERROR_CODE,
    REG_FROST_PROTECTION,
    REG_FROST_PROTECTION_STATUS,
    REG_HUMIDITY_ACTUAL,
    REG_INFRARED_MIX_STATUS,
    REG_MODULE_SOFTWARE_VERSION,
    REG_SAUNA_PROFILE,
    REG_SERVER_CONNECTION,
    REG_SESSION_TIME,
    REG_TEMPERATURE_ACTUAL,
    REG_TEMPERATURE_SET,
    REG_VAPORIZER_HUMIDITY,
    REG_VENTILATION_STATE,
    REG_VENTILATION_TIME,
    REG_WIFI_CONNECTION,
    SAUNA_PROFILES,
    STATUS_NAMES,
)

_LOGGER = logging.getLogger(__name__)




class FFESSaunaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching FFES Sauna data."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        slave: int,
        name: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=update_interval,
        )
        self.host = host
        self.port = port
        self.slave = slave
        self._client: ModbusTcpClient | None = None
        self._connect()

    def _connect(self) -> None:
        """Connect to the Modbus device."""
        try:
            self._client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=5,
            )
            _LOGGER.debug("Modbus client created for %s:%s", self.host, self.port)
        except Exception as err:
            _LOGGER.error("Error creating Modbus client: %s", err)
            raise

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Modbus device."""
        try:
            return await self.hass.async_add_executor_job(self._read_registers)
        except ModbusException as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error reading Modbus registers: %s", err)
            raise UpdateFailed(f"Error reading Modbus registers: {err}") from err

    def _read_registers(self) -> dict[str, Any]:
        """Read all necessary registers from the device."""
        data = {}

        try:
            # Read 16-bit holding registers (addresses 0-49)
            result = self._client.read_holding_registers(
                address=0,
                count=50,
                unit=self.slave
            )
            
            if result.isError():
                raise ModbusException(f"Error reading holding registers: {result}")

            registers = result.registers

            # Parse temperature values
            data["temperature_set"] = registers[REG_TEMPERATURE_SET]
            data["temperature_actual"] = registers[REG_TEMPERATURE_ACTUAL]
            
            # Parse profile
            profile_num = registers[REG_SAUNA_PROFILE]
            data["profile"] = SAUNA_PROFILES.get(profile_num, "unknown")
            data["profile_number"] = profile_num
            
            # Parse times
            data["session_time"] = registers[REG_SESSION_TIME]
            data["ventilation_time"] = registers[REG_VENTILATION_TIME]
            
            # Parse aromatherapy and humidity
            data["aromatherapy"] = registers[REG_AROMA_SET_VALUE]
            data["vaporizer_humidity_set"] = registers[REG_VAPORIZER_HUMIDITY]
            data["humidity_actual"] = registers[REG_HUMIDITY_ACTUAL]
            
            # Parse error code
            error_code = registers[REG_ERROR_CODE]
            data["error_code"] = error_code
            data["error_message"] = ERROR_CODES.get(error_code, f"Unknown error: {error_code}")
            data["has_error"] = error_code != 0
            
            # Parse CPIR settings
            data["cpir_group_1"] = registers[REG_CPIR_GROUP_1_SET]
            data["cpir_group_2"] = registers[REG_CPIR_GROUP_2_SET]
            data["cpir_g1_power"] = registers[REG_CPIR_G1_POWER]
            data["cpir_g2_power"] = registers[REG_CPIR_G2_POWER]
            data["cpir_g3_power"] = registers[REG_CPIR_G3_POWER]
            data["cpir_g4_power"] = registers[REG_CPIR_G4_POWER]
            
            # Parse controller status
            status_num = registers[REG_CONTROLLER_STATUS]
            data["controller_status"] = status_num
            data["controller_status_name"] = STATUS_NAMES.get(status_num, "Unknown")
            
            # Parse software version and model
            data["software_version"] = registers[REG_MODULE_SOFTWARE_VERSION]
            data["controller_model"] = registers[REG_CONTROLLER_MODEL]

            # Read coil registers (1-bit values)
            coil_result = self._client.read_coils(
                address=0,
                count=56,
                unit=self.slave
            )
            
            if coil_result.isError():
                raise ModbusException(f"Error reading coils: {coil_result}")

            coils = coil_result.bits
            
            # Parse coil states
            data["wifi_connection"] = coils[REG_WIFI_CONNECTION]
            data["server_connection"] = coils[REG_SERVER_CONNECTION]
            data["frost_protection"] = coils[REG_FROST_PROTECTION]
            data["frost_protection_status"] = coils[REG_FROST_PROTECTION_STATUS]
            data["ventilation_state"] = coils[REG_VENTILATION_STATE]
            data["infrared_mix_status"] = coils[REG_INFRARED_MIX_STATUS]

            _LOGGER.debug("Successfully read registers: %s", data)
            return data

        except ModbusException:
            raise
        except Exception as err:
            _LOGGER.error("Error parsing Modbus data: %s", err)
            raise ModbusException(f"Error parsing Modbus data: {err}") from err

    def _write_register_sync(self, address: int, value: int) -> None:
        """Synchronously write a register."""
        result = self._client.write_register(
            address=address,
            value=value,
            unit=self.slave
        )
        
        if result.isError():
            raise ModbusException(f"Error writing register {address}: {result}")
        
        _LOGGER.debug("Wrote value %s to register %s", value, address)

    def _write_coil_sync(self, address: int, value: bool) -> None:
        """Synchronously write a coil."""
        result = self._client.write_coil(
            address=address,
            value=value,
            unit=self.slave
        )
        
        if result.isError():
            raise ModbusException(f"Error writing coil {address}: {result}")
        
        _LOGGER.debug("Wrote value %s to coil %s", value, address)

    async def async_write_register(self, address: int, value: int) -> None:
        """Write a single register."""
        try:
            await self.hass.async_add_executor_job(
                self._write_register_sync, address, value
            )
            # Request data refresh after write
            await self.async_request_refresh()
        except ModbusException as err:
            _LOGGER.error("Error writing register %s: %s", address, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error writing register %s: %s", address, err)
            raise

    async def async_write_coil(self, address: int, value: bool) -> None:
        """Write a single coil."""
        try:
            await self.hass.async_add_executor_job(
                self._write_coil_sync, address, value
            )
            # Request data refresh after write
            await self.async_request_refresh()
        except ModbusException as err:
            _LOGGER.error("Error writing coil %s: %s", address, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error writing coil %s: %s", address, err)
            raise

    async def async_shutdown(self) -> None:
        """Shutdown coordinator."""
        if self._client:
            await self.hass.async_add_executor_job(self._client.close)
            _LOGGER.debug("Modbus client closed")