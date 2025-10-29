# 🔄 Instrukcja Aktualizacji do v1.0.1

## ⚠️ Jeśli masz zainstalowaną wersję 1.0.0:

### KROK 1: Usuń starą integrację
1. Settings → Devices & Services
2. Znajdź "FFES Sauna"
3. Kliknij trzy kropki → "Delete"
4. Potwierdź

### KROK 2: Usuń starą wersję z HACS (jeśli instalowałeś przez HACS)
1. HACS → Integrations
2. Znajdź "FFES Sauna"
3. Kliknij trzy kropki → "Uninstall"

### KROK 3: Restart Home Assistant
Settings → System → Restart

### KROK 4: Zainstaluj nową wersję
1. **Przez HACS:**
   - HACS → Integrations → ⋮ → Redownload
   - Wybierz wersję 1.0.1
   - Restart HA

2. **Lub ręcznie:**
   - Usuń folder `custom_components/ffes_sauna`
   - Rozpakuj nową wersję
   - Skopiuj do `custom_components/ffes_sauna`
   - Restart HA

### KROK 5: Dodaj integrację ponownie
1. Settings → Devices & Services → Add Integration
2. Szukaj "FFES Sauna"
3. Wprowadź dane:
   - IP: 192.168.0.208
   - Port: 502
   - Slave ID: 1
   - Name: My Sauna
4. Submit

✅ **Powinno działać!**

---

## 🆕 Dla nowych użytkowników:

Po prostu pobierz i zainstaluj - wszystkie problemy zostały naprawione! 🎉

### Co zostało naprawione w v1.0.1:

✅ **Naprawiono konflikt pymodbus** - zmieniono z `==3.6.8` na `>=3.6.0`  
✅ **Naprawiono błąd 500** - uproszczono config flow  
✅ **Dodano ikonę SVG** - ładna ikona sauny  
✅ **Zaktualizowano dokumentację**  

---

## 📝 Changelog:

### v1.0.1 (2025-10-29)
- Fixed: pymodbus version conflict (changed to >=3.6.0)
- Fixed: 500 Internal Server Error in config flow
- Added: Custom SVG icon
- Changed: Simplified config flow (no connection validation during setup)

### v1.0.0 (2025-10-29)
- Initial release

---

## 🆘 Nadal są problemy?

**Sprawdź logi:**
```yaml
logger:
  logs:
    custom_components.ffes_sauna: debug
    pymodbus: debug
```

**Weryfikuj połączenie:**
- Ping 192.168.0.208
- Sprawdź czy port 502 jest otwarty
- Sprawdź Slave ID (zazwyczaj 1)

**Zgłoś błąd:**
https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant/issues

---

**Wersja**: 1.0.1  
**Data**: 2025-10-29  
**Status**: ✅ GOTOWE!
