# 🔍 Risk Search Tool - Cloud Edition

> Centralized company risk screening with cloud-based keyword management and auto-updates

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourcompany/risk-search-tool)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ Features

- ✅ **32 High-Risk Keywords** across 6 categories (Financial Crime, Legal, Human Rights, Environmental, Governance, Cyber)
- ☁️ **Cloud-Based Keywords** - Update keywords in OneDrive, changes reflect instantly for all users
- 📊 **Centralized Search History** - All searches saved to shared Excel file
- 🔄 **Auto-Update** - Application updates automatically from GitHub
- 🚀 **No Installation** - Just Python + one click to run
- 👥 **Multi-User** - Entire team uses same keyword list and sees all searches
- 📥 **Excel Export** - Download complete search history anytime

---

## 🚀 Quick Start (For Users)

### **Option 1: One-Click Launch (Easiest)**

**Windows:**
```
1. Download ZIP from GitHub
2. Extract folder
3. Double-click launcher.bat
```

**Mac/Linux:**
```
1. Download ZIP from GitHub
2. Extract folder
3. Right-click launcher.sh → Open With → Terminal
```

### **Option 2: Command Line**

```bash
# Clone repository
git clone https://github.com/yourcompany/risk-search-tool.git
cd risk-search-tool

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

The app will open at: `http://127.0.0.1:5000`

---

## 📋 Prerequisites

- Python 3.8 or higher ([Download](https://www.python.org/downloads/))
- Internet connection (for OneDrive sync and updates)
- Web browser

---

## 🎯 How It Works

```
┌─────────────┐
│   OneDrive  │  ← Developers update keywords here
│             │
│ keywords.xlsx │
│ master_records.xlsx │
│ version.json │
└──────┬──────┘
       │
       │ Cloud Sync
       │
       ▼
┌─────────────┐
│  Your PC    │  ← App runs here
│             │
│  Risk Search │
│    Tool     │
└──────┬──────┘
       │
       │ Opens browser
       │
       ▼
┌─────────────┐
│  Browser    │  ← You work here
│             │
│  Search UI  │
└─────────────┘
```

### **User Workflow:**

1. **Launch app** → Checks for updates automatically
2. **Downloads keywords** from OneDrive (cached for 1 hour)
3. **Enter company names** → Comma-separated list
4. **Click "Generate Search Links"** → Creates Google search URLs
5. **Searches open in tabs** → Review results
6. **History saved** to OneDrive → Entire team can see

---

## 📊 Architecture

### **Components:**

| Component | Purpose | Location |
|-----------|---------|----------|
| **app.py** | Flask web server | Local |
| **cloud_sync.py** | OneDrive integration | Local |
| **auto_updater.py** | GitHub updates | Local |
| **config.py** | Settings & links | Local |
| **keywords.xlsx** | Keyword database | OneDrive |
| **master_records.xlsx** | Search history | OneDrive |
| **version.json** | Version control | OneDrive |

### **Data Flow:**

```
User Input → Flask → CloudSync → OneDrive → Excel
                               ↓
                         Google Search
```

---

## 🔧 Configuration

### **For Administrators:**

1. **Set up OneDrive files** (see [ONEDRIVE_SETUP_GUIDE.md](ONEDRIVE_SETUP_GUIDE.md))
2. **Get direct download links**
3. **Update config.py:**

```python
ONEDRIVE_CONFIG = {
    "keywords_url": "https://onedrive.live.com/download?resid=...",
    "master_records_url": "https://onedrive.live.com/download?resid=...",
    "version_url": "https://onedrive.live.com/download?resid=...",
}
```

4. **Create GitHub repository**
5. **Share with team**

---

## 📚 Documentation

- [📘 Deployment Guide](DEPLOYMENT_GUIDE.md) - For developers
- [☁️ OneDrive Setup Guide](ONEDRIVE_SETUP_GUIDE.md) - Cloud configuration
- [🔄 Update Process](#updating) - How to update keywords and code

---

## 🔄 Updating

### **For Developers:**

**Update Keywords:**
1. Edit `keywords.xlsx` in OneDrive
2. Add/remove rows or set Active = TRUE/FALSE
3. Save file
4. Changes reflect immediately for all users (after cache expires)

**Update Application:**
1. Make code changes locally
2. Test thoroughly
3. Commit to GitHub: `git push origin main`
4. Update `version.json` in OneDrive with new version number
5. Users auto-update next time they launch

**Example version.json:**
```json
{
  "version": "1.0.1",
  "release_date": "2025-02-11",
  "changes": [
    "Added 5 new environmental keywords",
    "Fixed search URL encoding",
    "Improved error messages"
  ],
  "critical_update": false
}
```

### **For Users:**

Just launch the app - it updates automatically! 🎉
---

## 🔐 Security

- ✅ OneDrive files require access permissions
- ✅ Only authorized users can edit keywords
- ✅ Search history visible to team (not public)
- ✅ No sensitive data stored in code
- ✅ HTTPS connections for OneDrive

**Best Practices:**
- Use Business OneDrive for better access control
- Set "edit" permissions only for developers on keywords.xlsx
- Regularly review access logs
- Keep repository private if it contains sensitive config

---

## 🎓 Usage Example

**Scenario:** You need to screen 3 companies

**Steps:**
1. Launch app
2. Enter: `HNBA, Celinco Life, Vallibel Finance`
3. Click "Generate Search Links"
4. 3 Google search tabs open, each with company name + all 32 keywords
5. Review results
6. Search recorded in master_records.xlsx with timestamp, username, and URL

**Search URL Format:**
```
"Company Name" (fraud OR corruption OR bribery OR ... OR leaked documents)
```

---

## 🆘 Troubleshooting

### **App won't start**
- Check Python installation: `python --version`
- Install dependencies: `pip install -r requirements.txt`

### **Keywords not loading**
- Check internet connection
- Verify OneDrive links in config.py
- Test link in browser (should download Excel file)

### **Updates not working**
- Check GitHub repository access
- Verify version.json is accessible
- Enable auto_update in config.py

### **Can't write to master_records.xlsx**
- Close file if open in Excel
- Check OneDrive sync status
- Verify write permissions

---

## 📞 Support

- **Installation Help:** [rashmikaakila100@gmail.com]

---

## 🔮 Roadmap

- [ ] Advanced search filters (by date range, category)
- [ ] Export to PDF reports
- [ ] Email notifications for high-risk findings
- [ ] Integration with internal compliance systems
- [ ] Mobile app version
- [ ] AI-powered risk scoring

## 👥 Contributors

- **Utharan Thavayoganathan, Aruna Udaya** - Guidance
- **Rashmika Hettiarachchi** - Initial development
- **Digital Forensic Team** - Deployment support

---

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- OneDrive integration via [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)
- Excel handling with [openpyxl](https://openpyxl.readthedocs.io/)

---

## 📝 Changelog

### **v1.0.0 (2025-02-10)**
- Initial cloud-enabled release
- OneDrive keyword management
- Auto-update functionality
- Centralized search history

---

## ⭐ Star this repo if it helped you!

Made by Rashmika Hettiarachchi (Analyst, KPMG)
