# Quick Start Guide - FFES Sauna Modbus Integration

## 1. Installation via HACS

1. Open HACS in Home Assistant
2. Click "Integrations"
3. Click the ⋮ menu (three dots) in top right
4. Select "Custom repositories"
5. Add repository URL: `https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant`
6. Category: "Integration"
7. Click "Add"
8. Find "FFES Sauna" and click "Download"
9. **Restart Home Assistant**

## 2. Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"FFES Sauna"**
4. Enter configuration:
   - **IP Address**: `192.168.0.208` (your controller IP)
   - **Port**: `502` (default Modbus TCP)
   - **Slave ID**: `1` (usually 1)
   - **Name**: `My Sauna` (any name you want)
   - **Scan Interval**: `10` (seconds, 5-120)
5. Click **Submit**

## 3. First Test

After configuration, you should see these entities:

### Main Control
- `climate.my_sauna_thermostat` - Temperature control
- `switch.my_sauna_power` - Power on/off

### Try This:
```yaml
# Turn on sauna in Developer Tools → Services
service: switch.turn_on
target:
  entity_id: switch.my_sauna_power

# Or set temperature
service: climate.set_temperature
target:
  entity_id: climate.my_sauna_thermostat
data:
  temperature: 85
```

## 4. Basic Automation

Create your first automation to start sauna when arriving home:

```yaml
alias: "Start Sauna When Home"
trigger:
  - platform: state
    entity_id: person.you
    to: "home"
action:
  - service: ffes_sauna.start_session
    target:
      entity_id: climate.my_sauna_thermostat
    data:
      profile: 2  # Dry sauna
      temperature: 85
      duration: 90
```

## 5. Dashboard Card

Add this to your dashboard:

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.my_sauna_thermostat
  - type: entities
    entities:
      - entity: sensor.my_sauna_current_temperature
      - entity: sensor.my_sauna_humidity
      - entity: number.my_sauna_session_time
      - entity: select.my_sauna_profile
```

## 6. Useful Services

### Start Session
```yaml
service: ffes_sauna.start_session
target:
  entity_id: climate.my_sauna_thermostat
data:
  profile: 2      # 2 = Dry Sauna
  temperature: 85
  duration: 60
```

### Stop Session
```yaml
service: ffes_sauna.stop_session
target:
  entity_id: climate.my_sauna_thermostat
```

### Change Profile
```yaml
service: ffes_sauna.set_profile
target:
  entity_id: climate.my_sauna_thermostat
data:
  profile: "wet_sauna"
```

## 7. Sauna Profiles

| Number | Name | Description |
|--------|------|-------------|
| 1 | infrared | Infrared Sauna (30-60°C) |
| 2 | dry_sauna | Traditional Dry Sauna (30-110°C) |
| 3 | wet_sauna | Wet Sauna (30-65°C) |
| 4 | ventilation | Ventilation Only |
| 5 | steam_bath | Steam Bath (20-50°C) |
| 6 | infrared_cpir | Infrared CPIR |
| 7 | infrared_mix | Infrared MIX |

## 8. Troubleshooting

### Can't connect?
- Verify IP address: ping `192.168.0.208`
- Check port 502 is open
- Verify Modbus TCP is enabled on controller

### Entities not updating?
- Check logs: Settings → System → Logs
- Enable debug logging:
  ```yaml
  logger:
    logs:
      custom_components.ffes_sauna: debug
  ```

### Read errors?
- Verify Slave ID (usually 1)
- Check firmware version (need 1.21/6.21+)

## 9. Next Steps

- Read full [README.md](README.md) for all features
- Check [automation examples](README.md#automation-examples)
- Join discussions on GitHub

## 10. Support

- 🐛 [Report bugs](https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant/issues)
- 💬 [Ask questions](https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant/discussions)
- ⭐ Star the project if you like it!

---

**Happy Sauna Sessions! 🧖‍♂️🔥**
