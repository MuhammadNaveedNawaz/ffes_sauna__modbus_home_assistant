# Contributing to FFES Sauna Modbus

Thank you for considering contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the issue
- Your Home Assistant version
- Your FFES controller model and firmware version
- Relevant log entries (enable debug logging)

### Suggesting Features

Feature suggestions are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- How it might work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if needed (README.md, code comments)
5. **Submit a pull request** with a clear description of your changes

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant development environment
- FFES Sauna controller for testing (or access to Modbus simulator)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant.git
cd ffes-sauna-modbus
```

2. Create a symbolic link in your Home Assistant config:
```bash
ln -s $(pwd)/custom_components/ffes_sauna ~/.homeassistant/custom_components/ffes_sauna
```

3. Restart Home Assistant and add the integration

### Testing

- Test all entity types (climate, sensor, switch, number, select, binary_sensor)
- Test all services (start_session, stop_session, set_profile)
- Test error handling (disconnect device, invalid values, etc.)
- Test with different sauna profiles
- Verify translations work correctly

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Home Assistant Guidelines

- Follow [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- Use async/await for I/O operations
- Properly handle exceptions
- Use coordinator pattern for data updates
- Add proper logging

### Code Example

```python
async def async_my_function(self) -> None:
    """Do something asynchronously."""
    try:
        result = await self.coordinator.write_register(address, value)
        _LOGGER.debug("Successfully wrote value: %s", value)
    except Exception as err:
        _LOGGER.error("Error writing register: %s", err)
        raise
```

### Documentation

- Add docstrings to all classes and functions
- Update README.md if adding new features
- Add examples for new services or entities
- Keep CHANGELOG.md updated

## Commit Messages

Use clear, descriptive commit messages:

```
Add support for CPIR group 5

- Add REG_CPIR_G5_POWER register constant
- Create number entity for group 5 control
- Update documentation with group 5 usage
```

### Commit Message Format

- Use imperative mood ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line
- Detailed description if needed
- Reference issues: "Fixes #123" or "Closes #456"

## Code Review Process

1. All pull requests require review before merging
2. Automated checks must pass (GitHub Actions)
3. At least one maintainer approval required
4. Address review feedback promptly

## Community Guidelines

- Be respectful and constructive
- Help others when possible
- Share your knowledge
- Have fun! 🎉

## Questions?

Feel free to open an issue for questions or join the discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FFES Sauna Modbus! 🙏
