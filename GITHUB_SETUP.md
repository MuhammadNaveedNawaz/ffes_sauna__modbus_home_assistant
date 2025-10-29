# GitHub Setup Guide
## How to Publish FFES Sauna Integration to GitHub

This guide will help you publish your FFES Sauna integration to GitHub and make it available via HACS.

## Prerequisites

- GitHub account
- Git installed on your computer
- The `ffes-sauna-modbus` project files

## Step 1: Create GitHub Repository

1. **Go to GitHub**
   - Navigate to https://github.com
   - Log in to your account

2. **Create New Repository**
   - Click the "+" icon in top right
   - Select "New repository"
   
3. **Repository Settings**
   - **Repository name**: `ffes-sauna-modbus`
   - **Description**: `Home Assistant integration for FFES Sauna controllers via Modbus TCP`
   - **Visibility**: ✅ Public (required for HACS)
   - **Initialize**: ❌ Do NOT initialize with README (we have our own)
   - Click "Create repository"

## Step 2: Upload Files to GitHub

### Option A: Using Git Command Line

```bash
# Navigate to your project directory
cd /path/to/ffes-sauna-modbus

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial release v1.0.0"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ffes-sauna-modbus.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. File → Add Local Repository
3. Choose the `ffes-sauna-modbus` folder
4. Click "Publish repository"
5. Uncheck "Keep this code private"
6. Click "Publish repository"

### Option C: Using GitHub Web Interface

1. Extract the ZIP file
2. Go to your new repository on GitHub
3. Click "uploading an existing file"
4. Drag and drop all files from the extracted folder
5. Commit changes

## Step 3: Create Release

1. **Go to Releases**
   - In your repository, click "Releases" (right sidebar)
   - Click "Create a new release"

2. **Tag Configuration**
   - **Tag version**: `v1.0.0`
   - **Target**: `main` branch
   - **Release title**: `v1.0.0 - Initial Release`

3. **Release Description**
   Copy and paste:
   ```markdown
   # FFES Sauna Modbus Integration v1.0.0
   
   Initial release of the FFES Sauna integration for Home Assistant.
   
   ## Features
   - ✅ Full temperature control via climate entity
   - ✅ Support for all 7 sauna profiles
   - ✅ Session timer management (1-2000 minutes)
   - ✅ Humidity control for wet sauna
   - ✅ Aromatherapy intensity control
   - ✅ CPIR infrared group controls
   - ✅ Error monitoring and display
   - ✅ Ventilation control
   - ✅ Frost protection mode
   - ✅ GUI configuration via config flow
   - ✅ Polish and English translations
   
   ## Installation
   
   Via HACS:
   1. Add custom repository: `https://github.com/YOUR_USERNAME/ffes-sauna-modbus`
   2. Install "FFES Sauna"
   3. Restart Home Assistant
   4. Add integration via UI
   
   See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed instructions.
   
   ## Requirements
   - Home Assistant 2024.1.0+
   - FFES Sauna Controller with Modbus TCP
   - Firmware 1.21/6.21 or newer
   
   ## Documentation
   - 📖 [README.md](README.md) - Full documentation
   - 🚀 [QUICK_START.md](QUICK_START.md) - Quick start guide
   - 💾 [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Installation guide
   - 📝 [example_configuration.yaml](example_configuration.yaml) - Example configs
   ```

4. **Attach Assets** (Optional)
   - Upload the `ffes-sauna-modbus.zip` file

5. **Publish Release**
   - Click "Publish release"

## Step 4: Update Repository Files

Update these files with your GitHub username:

### 1. README.md
Replace all instances of `YOUR_USERNAME` with your actual GitHub username:
```markdown
https://github.com/YOUR_USERNAME/ffes-sauna-modbus
```

### 2. hacs.json
No changes needed - HACS will find the repository automatically.

### 3. manifest.json
Update the URLs:
```json
{
  "documentation": "https://github.com/YOUR_USERNAME/ffes-sauna-modbus",
  "issue_tracker": "https://github.com/YOUR_USERNAME/ffes-sauna-modbus/issues",
  "codeowners": ["@YOUR_USERNAME"]
}
```

Commit and push these changes:
```bash
git add .
git commit -m "Update repository URLs"
git push
```

## Step 5: Configure Repository Settings

### 1. Enable Issues
- Settings → General → Features
- ✅ Enable "Issues"

### 2. Enable Discussions (Optional)
- Settings → General → Features
- ✅ Enable "Discussions"

### 3. Add Topics
- Main page → About (⚙️ gear icon)
- Add topics: `home-assistant`, `hacs`, `integration`, `sauna`, `modbus`, `smart-home`

### 4. Set Repository Description
- Settings → General
- Description: "Home Assistant integration for FFES Sauna controllers via Modbus TCP"
- Website: Leave empty or add your website

## Step 6: Make Repository HACS Compatible

Your repository is already HACS-compatible! It includes:
- ✅ `hacs.json` file
- ✅ `info.md` file
- ✅ Proper directory structure
- ✅ `manifest.json` with all required fields

## Step 7: Users Can Now Install

Users can add your integration to HACS:

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click ⋮ menu → Custom repositories
4. Add: `https://github.com/YOUR_USERNAME/ffes-sauna-modbus`
5. Category: Integration
6. Install and enjoy!

## Step 8: Promote Your Integration

### 1. Add to Home Assistant Community

Post in the forums:
- https://community.home-assistant.io/c/third-party/9

### 2. Share on Reddit
- r/homeassistant
- r/smarthome

### 3. Add to awesome-home-assistant
Submit a PR to add your integration to the list.

## Maintenance

### Creating New Releases

When you make updates:

1. Update version in `manifest.json`:
   ```json
   "version": "1.1.0"
   ```

2. Update `CHANGELOG.md`:
   ```markdown
   ## [1.1.0] - 2025-XX-XX
   ### Added
   - New feature X
   ### Fixed
   - Bug Y
   ```

3. Commit changes:
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git push
   ```

4. Create new release on GitHub:
   - Tag: `v1.1.0`
   - Title: `v1.1.0 - Feature Update`
   - Describe changes

### Responding to Issues

Monitor your GitHub issues:
- Enable notifications
- Respond within 1-2 days
- Label issues appropriately
- Close resolved issues

## Troubleshooting

### HACS Doesn't Find Repository

**Check:**
- Repository is public
- `hacs.json` is in root directory
- Repository has at least one release

### Validation Fails

Run validation locally:
```bash
# Install hassfest
pip install homeassistant

# Run validation
python -m homeassistant.scripts.hassfest custom_components/ffes_sauna
```

## Additional Resources

- [HACS Documentation](https://hacs.xyz/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [GitHub Documentation](https://docs.github.com/)

## Quick Reference

### Important URLs to Update

Replace `YOUR_USERNAME` in:
- [ ] README.md (all links)
- [ ] QUICK_START.md (installation link)
- [ ] INSTALLATION_GUIDE.md (repository links)
- [ ] manifest.json (documentation, issue_tracker, codeowners)
- [ ] This file (GITHUB_SETUP.md)

### Repository Checklist

- [x] Files uploaded to GitHub
- [ ] First release created (v1.0.0)
- [ ] README has correct GitHub username
- [ ] manifest.json has correct URLs
- [ ] Issues enabled
- [ ] Topics added
- [ ] Repository is public
- [ ] HACS compatible

---

**Congratulations! Your integration is now live on GitHub! 🎉**

Users can now install it via HACS and control their FFES saunas with Home Assistant!
