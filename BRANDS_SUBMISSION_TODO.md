# Brands Repo Submission - TODO

## Stan aktualny (2025-10-30)

✅ **Ukończone:**
- Integracja działa poprawnie
- GitHub Actions HACS validation PASSED (tylko brands check failed)
- Hassfest validation PASSED
- Release v1.0.6 opublikowany
- Ikona 512x512 przygotowana (`icon.png`)
- Skopiowano jako `icon@2x.png`

## Co pozostało do zrobienia:

### 1. Przygotowanie ikon (5 minut)

Masz `icon.png` (512x512) i `icon@2x.png` (512x512).

**MUSISZ ZROBIĆ:**
- Zmniejsz oryginalny `icon.png` do **256x256 px**
  - Wejdź: https://www.simpleimageresizer.com/
  - Upload `icon.png`
  - Resize to: 256x256 pixels
  - Pobierz i zastąp stary `icon.png`

**PLIKI FINALNE:**
- `icon.png` - 256x256 px (normalny DPI)
- `icon@2x.png` - 512x512 px (high DPI) - już masz

### 2. Fork brands repo (2 minuty)

- Wejdź: https://github.com/home-assistant/brands
- Kliknij "Fork" (prawy górny róg)
- Poczekaj aż fork się utworzy

### 3. Dodaj pliki do brands (10 minut)

W **swoim forku** brands:

**A. Utwórz manifest:**
1. Wejdź do folderu `custom_integrations/`
2. Kliknij "Add file" → "Create new file"
3. Nazwa pliku: `ffes_sauna/manifest.json`
4. Zawartość:
```json
{
  "domain": "ffes_sauna",
  "name": "FFES Sauna Modbus",
  "is_built_in": false
}
```
5. Commit: "Add ffes_sauna integration"

**B. Upload ikony:**
1. Wejdź do `custom_integrations/ffes_sauna/`
2. Kliknij "Add file" → "Upload files"
3. Przeciągnij/wybierz:
   - `icon.png` (256x256)
   - `icon@2x.png` (512x512)
4. Commit: "Add ffes_sauna icons"

### 4. Utwórz Pull Request (5 minut)

**A. W swoim forku:**
- Kliknij "Contribute" → "Open pull request"

**B. Title:**
```
Add ffes_sauna custom integration
```

**C. Description (skopiuj i wklej):**
```markdown
## Proposed change

Adding FFES Sauna Modbus custom integration to brands repository.

This integration provides Home Assistant support for FFES Sauna controllers via Modbus TCP protocol, enabling climate control, monitoring, and automation for FFES sauna systems.

## Type of change

- [x] Add a new logo or icon for a custom integration (custom component)
  - [x] I've added a link to my custom integration repository in the PR description

## Additional information

- This PR fixes or closes issue: N/A
- Link to code base pull request: N/A
- Link to documentation pull request: N/A
- Link to integration documentation on our website: N/A
- Link to custom integration repository: https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant

## Checklist

- [x] The added/replaced image(s) are **PNG**
- [x] Icon image size is 256x256px (`icon.png`)
- [x] hDPI icon image size is 512x512px for  (`icon@2x.png`)
- [ ] Logo image size has min 128px, but max 256px, on the shortest side (`logo.png`)
- [ ] hDPI logo image size has min 256px, but max 512px, on the shortest side (`logo@2x.png`)
```

**D. Kliknij "Create pull request"**

### 5. Czekaj na approval (1-5 dni)

- Bot zweryfikuje automatycznie
- Maintainerzy zaakceptują
- Dostaniesz email gdy będzie merged

### 6. Po zaakceptowaniu brands - Submit do HACS (15 minut)

Dopiero gdy brands PR będzie **merged**:

**A. Fork hacs/default:**
- Wejdź: https://github.com/hacs/default
- Kliknij "Fork"

**B. Edytuj plik `integration`:**
1. W swoim forku wejdź do pliku `integration`
2. Kliknij ikonę ołówka (Edit)
3. Dodaj ALFABETYCZNIE (znajdź właściwe miejsce):
```
LeszekWroblowski/ffes_sauna__modbus_home_assistant
```
4. Commit: "Add LeszekWroblowski/ffes_sauna__modbus_home_assistant"

**C. Utwórz Pull Request:**
- Title: "Add ffes_sauna integration"
- Description: Wypełnij template z linkiem do repo

**D. Poczekaj na approval (2-7 dni)**

## Linki przydatne:

- **Twoje repo:** https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant
- **GitHub Actions:** https://github.com/LeszekWroblowski/ffes_sauna__modbus_home_assistant/actions
- **Brands repo:** https://github.com/home-assistant/brands
- **HACS default:** https://github.com/hacs/default
- **Image resizer:** https://www.simpleimageresizer.com/

## Pliki w projekcie:

- `icon.png` - obecnie 512x512 (ZMIEŃ na 256x256!)
- `icon@2x.png` - 512x512 (OK, nie zmieniaj)

## Status GitHub Actions:

✅ Hassfest - PASSED
✅ HACS validation - PASSED (tylko brands check failed)
⏳ Brands check - będzie OK po merged brands PR

---

**Start od punktu 1 jutro!** 🚀
