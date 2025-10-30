# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant custom integration for FFES Sauna controllers with Modbus TCP support. It provides climate control, monitoring, and automation capabilities for FFES sauna systems (firmware 1.21/6.21 and newer).

## Architecture

### Core Components

**FFESSaunaCoordinator** (`coordinator.py`): Central data coordinator that:
- Manages Modbus TCP client connection (pymodbus library)
- Polls sauna controller registers every 10 seconds (configurable)
- Reads both 16-bit holding registers (0-49) and 1-bit coils (0-55)
- Handles pymodbus version compatibility (v3.x uses `slave` parameter, v4.0+ uses `device_id`)
- Provides async write methods for both registers and coils
- Automatically reconnects and refreshes data after writes

**Platform Structure**: The integration uses Home Assistant's platform pattern:
- `__init__.py`: Entry point, coordinator setup, platform loading
- `config_flow.py`: UI-based configuration flow (host, port, slave ID, name, scan_interval)
- `climate.py`: Main thermostat entity with temperature control
- `sensor.py`: Temperature, humidity, status, error sensors
- `switch.py`: Power, ventilation, frost protection switches
- `number.py`: Session time, aromatherapy, CPIR group controls
- `select.py`: Sauna profile selection
- `binary_sensor.py`: Error, heating, WiFi/server connection status

### Modbus Communication

**Register Layout**:
- Holding registers (16-bit): Temperature, time, profiles, humidity, error codes, CPIR settings
- Coil registers (1-bit): Controller state, ventilation, connections, frost protection
- All register addresses in `const.py` are 0-indexed (REG[1] in docs = address 0)

**IMPORTANT - Register Addressing**: FFES controllers use a register offset:
- **Physical start address**: 1 (FFES REG[1] = Modbus physical address 1)
- **Register count**: 50 registers total (REG[1] to REG[50])
- All register addresses in `const.py` are **logical (0-based)** addresses
- `REGISTER_OFFSET = 1` is automatically added to convert logical → physical addresses
- Example: Logical address 0 (REG_TEMPERATURE_SET = REG[1]) → Physical Modbus address 1
- Example: Logical address 1 (REG_TEMPERATURE_ACTUAL = REG[2]) → Physical Modbus address 2

The coordinator reads all 50 holding registers in one call starting from physical address 1.

**Version Compatibility**: The coordinator detects pymodbus version at runtime:
- **pymodbus 3.0-3.9**: Uses `slave=` parameter
- **pymodbus 3.10+**: Uses `device_id=` parameter (slave was removed in 3.10.0)
- **pymodbus 4.0+**: Uses `device_id=` parameter

```python
if USE_DEVICE_ID:  # True for 3.10+ and 4.0+
    result = self._client.read_holding_registers(0, count=50, device_id=self.slave)
else:
    result = self._client.read_holding_registers(0, 50, slave=self.slave)
```

### Data Flow

1. Coordinator polls Modbus every scan_interval seconds
2. Reads all registers in two batches: holding registers (0-49) and coils (0-55)
3. Parses data into dictionary with semantic keys (temperature_actual, profile, error_code, etc.)
4. All platform entities inherit from `CoordinatorEntity` and access data via `self.coordinator.data`
5. Write operations use `coordinator.async_write_register()` or `async_write_coil()`, which trigger automatic refresh

## Development Commands

### Testing with Home Assistant

**No standalone tests**: This integration is tested by installing in Home Assistant:
```bash
# Copy to Home Assistant custom_components directory
cp -r custom_components/ffes_sauna /path/to/homeassistant/custom_components/

# Restart Home Assistant
# Then configure via UI: Settings → Devices & Services → Add Integration → "FFES Sauna"
```

**Debug Logging**: Add to Home Assistant `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.ffes_sauna: debug
    pymodbus: debug
```

### Version Bumping

When releasing:
1. Update version in `manifest.json`
2. Update `CHANGELOG.md` following Keep a Changelog format
3. Create git tag matching version

## Key Constants and Configuration

**Configuration Keys** (`const.py`):
- `CONF_SLAVE`: Modbus slave/unit ID (default: 1)
- `DEFAULT_PORT`: 502 (Modbus TCP standard)
- `DEFAULT_SCAN_INTERVAL`: 10 seconds

**Sauna Profiles** (7 types):
1. Infrared (30-60°C)
2. Dry Sauna (30-110°C)
3. Wet Sauna (30-65°C)
4. Ventilation (no temperature)
5. Steam Bath (20-50°C)
6. Infrared CPIR (30-60°C)
7. Infrared MIX (30-60°C)

**Error Codes**: 13 defined error codes in `ERROR_CODES` dict (0 = no error, 1-13 = various sensor/hardware errors)

## Important Implementation Details

### Pymodbus Version Handling

Always use the version detection pattern from `coordinator.py:52-68`. When calling any Modbus method:
- Check `USE_DEVICE_ID` flag (determined at module load time)
- Use `device_id=` parameter for v3.10+ and v4.0+
- Use `slave=` parameter for v3.0-3.9
- **Important**: Pymodbus 3.10.0 introduced breaking change: `slave=` was replaced with `device_id=`
- Home Assistant typically uses pymodbus 3.11.1+ which requires `device_id=` parameter

### Entity Device Info

All entities must share the same device_info identifiers:
```python
"device_info": {
    "identifiers": {(DOMAIN, entry.entry_id)},
    "name": entry.data["name"],
    "manufacturer": "FFES",
    "model": "Sauna Controller",
}
```

### Writing Values

Never write directly to Modbus client. Always use coordinator methods:
```python
# Use LOGICAL addresses (0-based) - REGISTER_OFFSET is added automatically
await self.coordinator.async_write_register(address, value)
await self.coordinator.async_write_coil(address, bool_value)
```
These methods:
- Handle version compatibility (slave vs device_id)
- Automatically add REGISTER_OFFSET to convert logical → physical addresses
- Handle error handling
- Trigger automatic data refresh

## Common Issues

**Error 500 on config flow**: Ensure config flow doesn't validate Modbus connection synchronously. Validation happens on first coordinator refresh.

**Modbus parameter errors**: The most common issue is incompatibility between pymodbus versions:
- Pymodbus 3.0-3.9 uses `slave=` parameter
- Pymodbus 3.10+ uses `device_id=` parameter (breaking change!)
- Home Assistant 2025.11+ uses pymodbus 3.11.1+ which requires `device_id=`
- The coordinator automatically detects the version and uses the correct parameter
- Error messages like "unexpected keyword argument 'slave'" mean you're using old parameter names with new pymodbus

**ILLEGAL DATA ADDRESS (Exception Code 2)**: This typically means incorrect register addressing:
- FFES controllers require **physical start address 1** (FFES REG[1] = Modbus address 1, not 0!)
- The coordinator uses `REGISTER_OFFSET = 1` to handle this automatically
- Logical addresses in code (0-based) are converted to physical addresses (1-based)
- If you get this error, verify you're using the coordinator's read/write methods, not direct Modbus calls

**QModMaster Testing**: When testing with QModMaster, use:
- Start address: 1 (to read FFES REG[1])
- Number of registers: 50
- Function: Read Holding Registers (0x03)

**Entity not updating**: Verify `scan_interval` setting and check Home Assistant logs for Modbus communication errors.

## Repository Structure

```
custom_components/ffes_sauna/
├── __init__.py           # Entry point, coordinator setup
├── coordinator.py        # Modbus communication and data management
├── const.py             # All constants, register addresses, profiles
├── config_flow.py       # UI configuration
├── climate.py           # Thermostat entity
├── sensor.py            # Sensor entities
├── switch.py            # Switch entities
├── number.py            # Number input entities
├── select.py            # Profile selector
├── binary_sensor.py     # Binary sensors
├── manifest.json        # Integration metadata
├── services.yaml        # Service definitions
├── strings.json         # UI strings
└── translations/        # Localization files
```
