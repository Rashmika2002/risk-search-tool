# 🔍 Risk Search Tool

> Comprehensive company risk screening with automated keyword search powered by Google Sheets

![Version](https://img.shields.io/badge/version-2.0.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Overview

The **Risk Search Tool** is an enterprise-grade application designed for KPMG teams to perform comprehensive risk assessments on companies. It automates Google searches using a selected keyword worksheet and maintains a centralized database of all searches in Google Sheets.

### ✨ Key Features

- 🔍 **Automated Risk Screening** - Choose between standard and Russian risk keyword sheets
- ☁️ **Cloud Database** - All data stored in Google Sheets (zero conflicts)
- 📊 **Real-time Collaboration** - Multiple users can search simultaneously
- 📥 **Excel Export** - Download your search history anytime
- 🔄 **Auto-Updates** - Application updates automatically from GitHub
- 🔐 **Secure** - Embedded credentials, no sensitive files exposed
- 💾 **Local Backup** - Automatic backup to local Excel files

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Git** ([Download here](https://git-scm.com/downloads))
- Internet connection

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/Rashmika2002/risk-search-tool.git
cd risk-search-tool

# 2. Run the application
# Windows:
RiskSearchTool.bat

```

That's it! The browser will open automatically.

---

## 📖 Usage

### Basic Search

1. **Enter company names** (comma-separated):
   ```
   HNBA, Ceylinco Life, Vallibel Finance
   ```

2. **Click "Generate Search Links"**

3. **Search tabs open automatically** - Review Google results

4. **Data saved to Google Sheets** - Accessible to entire team

### Download Your Searches

- Click **"Download My Searches"** button
- Excel file downloads with all your searches
- Includes: Company name, date, search URL, status

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   Flask Web App     │
│  (Port 5000)        │
└──────────┬──────────┘
           │
           ├─► Google Sheets API
           │   ├─ Searches (All users)
           │   └─ Keywords (Centralized)
           │
           ├─► Local Excel Backup
           │   └─ User's searches
           │
           └─► GitHub
               └─ Auto-updates
```

---

## 📊 Data Storage

### Google Sheets Structure

**Sheet 1: Risk Searches**
| ID | Client Name | Report Date | Username | Search URL | Status | Keywords | Version |
|----|-------------|-------------|----------|------------|--------|----------|---------|
| 1  | HNBA        | 2025-02-15  | john     | https://... | Success | 32       | 2.0.0   |

**Sheet 2: Keywords**
| Category | Keyword | Active |
|----------|---------|--------|
| Financial Crime | fraud | TRUE |
| Legal & Regulatory | lawsuit | TRUE |

**Sheet 3: Russian_Keyword_Sheet**
| Category | Keyword | Active |
|----------|---------|--------|
| Russian Risk | Blacklist | TRUE |
| Russian Risk | Russia | TRUE |

The app creates this worksheet and adds the supplied Russian-risk keywords the first time it connects if the worksheet does not already exist. In the app, choose **Russian_Keyword_Sheet** from the keyword sheet selector and click **Select Keyword Sheet** before searching. Set `Active = FALSE` in the worksheet to disable any term.

### Local Backup

Each user gets a local Excel backup:
```
C:\Users\{username}\.risk_search_tool\{username}_searches.xlsx

```

---

## ⚙️ Configuration

### Update Your Google Sheet ID

Edit `config.py` line 21:

```python
_SHEET_ID = "YOUR_GOOGLE_SHEET_ID"  # Replace this
```

**How to get Sheet ID:**
```
https://docs.google.com/spreadsheets/d/1abc123xyz456/edit
                                        ^^^^^^^^^^^^
                                        Copy this part
```

### Manage Keywords

1. Open your Google Sheet
2. Go to the "Keywords" or "Russian_Keyword_Sheet" tab
3. Add/edit/disable keywords:
   - Set `Active = TRUE` to use keyword
   - Set `Active = FALSE` to disable
4. Select the matching worksheet in the app before searching
5. Changes apply on the next search

---

## 🔄 Auto-Updates

The application checks GitHub for updates on startup.

### For Administrators

**Release a new version:**

1. Make your code changes
2. Update `version.json`:
   ```json
   {
     "version": "2.0.1",
     "changes": ["Fixed bug X", "Added feature Y"]
   }
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Release v2.0.1"
   git push origin main
   ```

Users' apps will auto-update on next launch!

---

## 🛡️ Security

### Credential Protection

- ✅ Credentials are **Base64 encoded** and embedded in code
- ✅ No separate `credentials.json` file
- ✅ Employees cannot easily extract credentials
- ✅ Good for internal company use

### What's NOT in GitHub

```
❌ credentials.json (original file - keep safe)
❌ encrypt_credentials.py (internal tool)
❌ .env files
```

### What's in GitHub (Safe)

```
✅ config.py (embedded encrypted credentials)
✅ app.py, cloud_sync.py (application code)
✅ version.json (version tracking)
✅ RiskSearchTool.bat (launcher)
```

---

## 📁 Project Structure

```
risk-search-tool/
├── app.py                      # Flask application
├── cloud_sync.py               # Google Sheets integration
├── auto_updater.py             # GitHub auto-updates
├── config.py                   # Configuration (embedded credentials)
├── requirements.txt            # Python dependencies
├── version.json                # Version tracking
├── RiskSearchTool.bat               # Windows launcher
├── README.md                   # This file
└── templates/
    └── index.html              # Web interface
```

---

## 🧩 Dependencies

```
Flask>=2.3.0
gspread>=5.12.0
google-auth>=2.25.0
openpyxl>=3.1.0
requests>=2.31.0
```

All installed automatically by `RiskSearchTool.bat`

---

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python from [python.org](https://www.python.org/downloads/)
- ⚠️ **Check "Add Python to PATH"** during installation
- Restart computer after installation

**"Google Sheets connection failed"**
- Verify Sheet ID in `config.py`
- Check service account has Editor access to sheet
- Ensure internet connection is active

**"Port 5000 already in use"**
- Close other Flask applications
- Or change port in `config.py`:
  ```python
  "port": 5001,  # Change to different port
  ```

**"Dependencies installation failed"**
- Run `RiskSearchTool.bat` as Administrator
- Or manually: `pip install -r requirements.txt`

---

## 📈 Statistics

- **32 Risk Keywords** across 6 categories
- **Zero Conflict** concurrent user support
- **Real-time** Google Sheets synchronization
- **Automatic** local Excel backups

---

## 🎓 For Developers

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Create New Release

```bash
# 1. Update the runtime version in app.py
APP_CONFIG['current_version'] = "2.0.2"

# 2. Keep the version in config.py in sync for new installations
APP_CONFIG = {
    "current_version": "2.0.2",  # Update this
}

# 3. Update version.json
{
  "version": "2.0.2",
  "changes": ["Your changes here"]
}

# 4. Commit and publish to both branches
git add .
git commit -m "Release v2.0.2"
git push origin HEAD:master
git push origin HEAD:main
```

The updater now reads releases from `master`. Keep the `main` branch updated with each release for installations that still use the legacy `main` update URL.

---

## 📞 Support

### For Employees

**Installation help:** Contact IT Support
**Bug reports:** Create GitHub issue
**Feature requests:** Create GitHub issue

### For Administrators

**Google Cloud issues:** Check service account permissions
**Sheet access:** Verify sharing settings
**Updates not working:** Check `version.json` in GitHub

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Sheets API** - Cloud database
- **Flask** - Web framework
- **Contributors** - Rashmika Akila (Analyst - Digital Forensics), Utharan Thavayoganathan (Manager - Digital Forensics), Aruna Udaya (3rd party consultant)      

---

## 🔗 Links

- **Repository:** https://github.com/Rashmika2002/risk-search-tool
- **Issues:** https://github.com/Rashmika2002/risk-search-tool/issues
- **Google Cloud Console:** https://console.cloud.google.com

---

## 📊 Version History

### v2.0.2 (2026-09-27)
- ✅ Added selectable Russian risk keyword sheet
- ✅ Improved update compatibility for existing installations

### v2.0.0 (2025-02-15)
- ✅ Moved to Google Sheets database
- ✅ Keywords managed in Google Sheets
- ✅ Embedded credentials for security
- ✅ Removed OneDrive dependency
- ✅ GitHub-based auto-updates
- ✅ Improved one-click launcher

### v1.0.0 (Initial Release)
- Basic search functionality
- Local file storage
- Manual keyword management

---

## 🚀 Quick Links

- [Installation](#installation-5-minutes)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

*For more information, visit the [Wiki](https://github.com/Rashmika2002/risk-search-tool/wiki)*
