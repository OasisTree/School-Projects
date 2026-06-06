# IsQueueNek ACP (Advanced Computer Project)

**Comprehensive scholarship management platform with GUI and Terminal implementations**

---

## Overview

The ACP folder contains two complete implementations of the IsQueueNek scholarship management system:

1. **GUI Based System** - Tkinter desktop application with visual interface
2. **Terminal Based System** - Command-line interface with menu navigation

Both implementations share the same core functionality but differ in presentation and deployment scenarios.

---

## Folder Structure

```
ACP/
├── GUI Based System/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── gui/
│   ├── utils/
│   ├── data/
│   └── README.md
│
├── Terminal Based System/
│   └── IsQueueNek/
│       ├── ver_1/
│       │   └── Centralized Scholarship Management System.py
│       │
│       └── ver_2/
│           ├── main.py
│           ├── config.py
│           ├── database.py
│           ├── admin/
│           ├── provider/
│           ├── student/
│           ├── utils/
│           ├── data/
│           └── README.md
│
└── README.md (this file)
```

---

## Quick Start

### GUI Version (Recommended for Desktop)

```bash
# Navigate to GUI folder
cd ACP/GUI\ Based\ System

# Run the application
python main.py
```

**Features:**
- Modern graphical interface
- Dark theme design
- Visual dashboards
- Easy navigation
- Responsive layout

---

### Terminal Version (Recommended for Server/Automation)

#### Version 2 (Latest - Recommended)
```bash
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_2
python main.py
```

#### Version 1 (Original)
```bash
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_1
python Centralized\ Scholarship\ Management\ System.py
```

**Features:**
- Menu-driven interface
- Lightweight and fast
- No GUI dependencies
- Server deployment friendly
- Automation compatible

---

## System Architecture

### Shared Components

Both implementations use similar architecture:

```
Entry Point (main.py)
        ↓
Configuration (config.py)
        ↓
Database Layer (database.py)
        ↓
Role-Specific Modules
├── admin/
├── provider/
└── student/
        ↓
Utilities (utils/)
├── id_generator.py
├── security.py
└── validators.py
        ↓
Data Storage (data/)
├── students.json
├── providers.json
└── admin.json
```

---

## User Roles

### Student
- Register with personal information
- Create master profile (academic & financial data)
- Browse eligible scholarships
- Apply to scholarships
- Track application status
- Upload supporting documents

### Provider
- Register as scholarship organization
- Wait for admin approval
- Create scholarship offerings
- Define eligibility requirements
- Review and manage applicants
- Track scholarship statistics

### Administrator
- Verify provider accounts
- Monitor system activity
- Manage user accounts
- Generate reports
- Ensure system integrity

---

## Features Comparison

| Feature | GUI | Terminal |
|---------|-----|----------|
| **Visual Interface** | Yes | No |
| **Dark Theme** | Yes | N/A |
| **Dashboards** | Yes | Text-based |
| **Menu Navigation** | Buttons | Text menus |
| **Performance** | Good | Very Fast |
| **Deployment** | Desktop | Desktop/Server |
| **Learning Curve** | Easy | Medium |
| **Memory Usage** | Moderate | Low |
| **Network Ready** | No | Yes (extendable) |

---

## Technologies Used

### Both Versions
- **Language**: Python 3.7+
- **Data Storage**: JSON files
- **Authentication**: SHA256 password hashing
- **Identifiers**: UUID generation

### GUI Version Only
- **Framework**: Tkinter
- **UI**: Modern dark theme
- **Windows**: Responsive layout
- **Components**: Custom widgets

### Terminal Version Only
- **Interface**: Menu-driven CLI
- **Input**: Text prompts
- **Output**: Console display
- **Navigation**: Numeric menu selection

---

## Requirements

### Python Version
```
Python 3.7 or higher
```

### Dependencies
```
tkinter (for GUI version, usually included with Python)
json (standard library)
hashlib (standard library)
uuid (standard library)
os (standard library)
```

### Installation Check
```bash
# Verify Python
python --version

# Verify tkinter (GUI only)
python -m tkinter

# If tkinter is missing:
# Ubuntu/Debian: sudo apt-get install python3-tk
# macOS: python3 -m pip install tk
# Windows: Usually included
```

---

## 🔄 Data Model

### Student Profile
```json
{
  "student_id": {
    "username": "string",
    "password": "hashed_string",
    "personal": {
      "first_name": "string",
      "last_name": "string",
      "email": "string"
    },
    "academic": {
      "gwa": "float",
      "program": "string"
    },
    "financial": {
      "annual_income": "integer",
      "location": "string"
    },
    "documents": ["file_paths"],
    "applications": ["scholarship_ids"]
  }
}
```

### Scholarship Profile
```json
{
  "scholarship_id": {
    "name": "string",
    "amount": "float",
    "organization": "string",
    "requirements": {
      "min_gwa": "float",
      "max_income": "integer",
      "location": "string",
      "available_slots": "integer"
    },
    "status": "active",
    "applications": ["student_ids"]
  }
}
```

---

## Security Features

### Authentication
- SHA256 password hashing
- Secure login validation
- Session management
- Account verification

### Data Protection
- File-based encryption ready
- Role-based access control
- Input validation
- Error handling

### Provider Verification
- Admin approval gate
- Status tracking (Pending/Approved/Rejected)
- Multi-step verification

---

## Sample Accounts

### Student Accounts
| Username | Password | ID |
|----------|----------|-----|
| dylan_luke | test123 | 26-1 |
| john_doe | pass123 | STU-001 |

### Provider Accounts
| Organization | Username | Password | ID |
|-------------|----------|----------|-----|
| DOST | dost_admin | dost123 | PROV-1 |
| CHED | ched_admin | ched123 | PROV-2 |
| Batangas | batangas_gov | bat123 | PROV-3 |
| Lipa | lipa_city | lipa123 | PROV-4 |

### Admin Account
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

---

## Workflows

### Student Workflow
```
Login/Register → Create Profile → Browse Scholarships → Apply → Track Status
```

### Provider Workflow
```
Register → Wait for Approval → Create Scholarship → Review Applicants → Manage
```

### Admin Workflow
```
Monitor System → Approve Providers → Manage Accounts → Generate Reports
```

---

## Data Files

All data is stored in JSON format in the `data/` directory:

```
data/
├── students.json       # Student profiles and applications
├── providers.json      # Provider accounts and scholarships
├── admin.json         # Administrator accounts
```

### Data Persistence
- **Load**: Automatic on application startup
- **Save**: Automatic on application exit
- **Backup**: Create backups before major changes

---

## Configuration

### GUI Version
- **Theme**: Dark mode (customizable in theme.py)
- **Window Size**: 1320x820 (default)
- **Minimum Size**: 1100x700

### Terminal Version
- **Menu Style**: Numeric selection
- **Display**: Text-based tables
- **Input**: Line-by-line prompts

---

## Troubleshooting

### Application Won't Start
```bash
# Verify Python
python --version

# Check tkinter (GUI only)
python -m tkinter

# Check file permissions
chmod +x main.py
```

### Login Issues
- Verify credentials in sample accounts
- Check JSON files in data/ folder
- Clear data files for fresh start

### Data Not Saving
- Check write permissions for data/ directory
- Verify sufficient disk space
- Ensure JSON syntax is valid

### Performance Issues
- Close other applications
- Check available memory
- Monitor system resources

---

## Deployment

### Desktop Deployment
1. Ensure Python 3.7+ installed
2. Copy entire folder to target machine
3. Run `python main.py` in appropriate version folder

### Server Deployment (Terminal Version)
1. Install Python 3.7+ on server
2. Copy files to server directory
3. Schedule startup or integrate with automation
4. Configure for remote access if needed

### Development Environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# No external packages needed!
```

---

## 📈 Future Enhancements

### Phase 2
- [ ] Web-based version
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Real-time chat

### Phase 3
- [ ] Machine learning matching
- [ ] Cloud database integration
- [ ] Multi-language support
- [ ] Video verification
- [ ] Payment processing

---

## 📊 Project Statistics

| Metric | GUI | Terminal |
|--------|-----|----------|
| Lines of Code | ~2000 | ~1500 |
| Data Files | 3 | 3 |
| Modules | 8 | 7 |
| Functions | 50+ | 45+ |
| User Roles | 3 | 3 |

---

## 🎓 Educational Value

### Concepts Covered
- GUI framework usage (Tkinter)
- CLI design and implementation
- JSON data persistence
- Authentication and security
- Role-based access control
- Database operations
- User interface design
- Algorithm optimization

### Skills Developed
- Python programming
- File handling
- JSON data manipulation
- User interface design
- System architecture
- Data modeling
- Security practices
- Testing and debugging

---

## 📞 Support & Documentation

### For GUI Version
- See: [GUI Based System README](GUI%20Based%20System/README.md)

### For Terminal Version (v2)
- See: [Terminal Version README](Terminal%20Based%20System/IsQueueNek/ver_2/README.md)

### For Terminal Version (v1)
- See original implementation documentation

---

## 📄 License & Attribution

Part of IsQueueNek project - Academic coursework for first-year Computer Science.

---

## ✅ Quick Reference

```bash
# GUI Version
cd ACP/GUI\ Based\ System
python main.py

# Terminal Version v2
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_2
python main.py

# Terminal Version v1
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_1
python Centralized\ Scholarship\ Management\ System.py
```

---

**Last Updated**: June 2026  
**Status**: Complete & Production Ready  
**Version**: 2.0
