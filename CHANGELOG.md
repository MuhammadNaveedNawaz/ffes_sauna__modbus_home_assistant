# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-29

### Added
- Initial release of FFES Sauna Home Assistant integration
- Climate entity for temperature control
- Support for all 7 sauna profiles (Infrared, Dry, Wet, Ventilation, Steam Bath, CPIR, MIX)
- Sensor entities for temperature, humidity, status, and error monitoring
- Switch entities for power, ventilation, frost protection, and infrared mix
- Number entities for session time, ventilation time, aromatherapy, humidity, and CPIR groups
- Select entity for profile selection
- Binary sensors for error, heating, frost protection, WiFi and server connection status
- Services: start_session, stop_session, set_profile
- Config flow for easy GUI configuration
- Support for Modbus TCP protocol
- Polish and English translations
- Comprehensive documentation and examples

### Features
- Real-time monitoring of sauna temperature and status
- Remote control of all sauna functions
- Session timer management (1-2000 minutes)
- Humidity control for wet sauna and steam bath
- Aromatherapy intensity control
- CPIR infrared group power control
- Error code detection and display
- Frost protection mode
- Ventilation control
- Multiple sauna profile support

### Technical
- Built on pymodbus 3.6.8
- Async/await architecture
- Polling-based updates with configurable scan interval (5-120 seconds)
- Proper error handling and logging
- HACS compatible structure
- Follows Home Assistant integration best practices

## [Unreleased]

### Planned Features
- Auto-discovery support
- Session history tracking
- Energy consumption monitoring (if supported by hardware)
- Advanced automation templates
- Dashboard card templates
- Additional language translations

---

**Note:** This integration is not officially affiliated with FFES. It is a community-developed project based on the Modbus TCP protocol specification.
