# Ikona dla integracji FFES Sauna

## ✅ Co zostało dodane:

1. **icon.svg** - Wektorowa ikona sauny z:
   - Budynkiem sauny (brązowy drewniany)
   - Drzwiami z klamką
   - Oknem
   - Falami ciepła/pary
   - Termometrem
   - Ikoną ognia
   - Logo "FFES"

2. **integration_type: "device"** w manifest.json

## 📸 Jak wygląda ikona:

Ikona pokazuje:
- 🏠 Drewniany budynek sauny
- 🌡️ Termometr
- 🔥 Płomienie
- 💨 Fale ciepła/pary

## 🎨 Kolory:

- Pomarańczowy (#FF6B35) - ogień/ciepło
- Brązowy (#8B4513) - drewno
- Czerwony (#FF4444) - temperatura
- Złoty (#FFD700) - akcenty

## 📱 Gdzie będzie widoczna:

1. **W HACS** - podczas przeglądania integracji
2. **W Settings → Integrations** - ikona obok nazwy
3. **Na kartach urządzenia** - w widoku urządzeń

## 🔧 Jeśli chcesz zmienić ikonę:

### Opcja 1: Użyj własnej ikony SVG/PNG
1. Stwórz plik `icon.png` (256x256 px) lub `icon.svg`
2. Umieść w: `custom_components/ffes_sauna/`
3. Zrestartuj Home Assistant

### Opcja 2: Użyj ikony Material Design
W plikach entity możesz użyć dowolnej ikony z:
https://pictogrammers.com/library/mdi/

Np. dla sauny:
- `mdi:sauna`
- `mdi:fire`
- `mdi:thermometer-high`
- `mdi:steam`

## ✨ Ikona jest już dodana!

Po wgraniu na GitHub i instalacji przez HACS, ikona pojawi się automatycznie! 🎉
