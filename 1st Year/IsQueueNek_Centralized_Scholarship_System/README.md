# IsQueueNek: Centralized Scholarship Management System

**IsQueueNek** is a comprehensive scholarship discovery and management platform designed to streamline the process of finding, applying for, and managing scholarships. The system serves as a centralized hub connecting student applicants with verified scholarship providers through a secure, efficient, and user-friendly interface.

---

## Problem Statement & Solution

### The Challenge
Traditional scholarship systems in the Philippines face critical challenges:
- **Fragmentation**: Scholarships scattered across multiple platforms
- **Inefficiency**: Manual verification and tedious documentation
- **Scam Vulnerability**: No verification of provider legitimacy
- **Data Redundancy**: Students submit same documents repeatedly
- **Lengthy Queues**: In-person document submission and waiting periods
- **Lack of Transparency**: Unclear application timelines and status

### Our Solution
IsQueueNek provides a centralized, secure, and automated digital platform that:
- **Verifies Providers**: Admin approval gate ensures legitimacy
- **Eliminates Redundancy**: Master Student Profile system
- **Digital-First**: Complete online application process
- **Smart Matching**: Automated eligibility-based recommendations
- **Real-Time Tracking**: Live application status updates
- **Document Attachments**: Local file uploads for verification

---

## Project Structure

```
IsQueueNek_Centralized_Scholarship_System/
│
├── ACP/                              # Advanced Computer Project
│   │
│   ├── GUI Based System/             # Desktop Application (Tkinter)
│   │   ├── main.py                   # Entry point
│   │   ├── config.py                 # Configuration
│   │   ├── database.py               # Data operations
│   │   ├── gui/                      # GUI components
│   │   │   ├── main_window.py
│   │   │   ├── admin/
│   │   │   ├── provider/
│   │   │   └── student/
│   │   ├── utils/
│   │   ├── data/                     # JSON databases
│   │   └── README.md
│   │
│   └── Terminal Based System/        # Command-Line Interface
│       └── IsQueueNek/
│           ├── ver_1/                # Original implementation
│           │   └── Centralized Scholarship Management System.py
│           │
│           └── ver_2/                # Improved implementation
│               ├── main.py
│               ├── config.py
│               ├── database.py
│               ├── admin/
│               ├── provider/
│               ├── student/
│               ├── utils/
│               ├── data/
│               └── README.md
│
├── DSA/                              # Data Structures & Algorithms
│   ├── IsQueueNek.cpp                # C++ implementation
│   ├── students.txt
│   ├── providers.txt
│   └── README.md
│
└── README.md                         # This file
```

---

## Quick Start

### Choose Your Implementation

#### Option 1: GUI Version (Desktop Application)
**Best for**: User-friendly interface, visual interaction
```bash
cd ACP/GUI\ Based\ System
python main.py
```
- Modern Tkinter interface
- Visual dashboards
- Dark theme UI
[Full GUI Documentation](ACP/README.md)

---

#### Option 2: Terminal Version (CLI)
**Best for**: Server deployment, automation, learning
```bash
# Version 2 (Recommended)
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_2
python main.py

# OR Version 1 (Original)
cd ACP/Terminal\ Based\ System/IsQueueNek/ver_1
python Centralized\ Scholarship\ Management\ System.py
```
- Command-line interface
- Lightweight and fast
- Easy automation
[Full Terminal Documentation](ACP/Terminal%20Based%20System/IsQueueNek/ver_2/README.md)

---

#### Option 3: C++ DSA Version
**Best for**: Algorithm study, performance optimization, systems programming
```bash
cd DSA
g++ -std=c++11 IsQueueNek.cpp -o isqueuenek
./isqueuenek
```
- Low-level data structures
- High performance
- Learning algorithms
[Full DSA Documentation](DSA/README.md)

---

## Key Features

### For Students
- **Master Student Profile**: Single entry, apply to unlimited scholarships
- **Smart Discovery**: Automated filtering by GWA, income, location
- **Document Upload**: Upload grades and income verification
- **One-Click Apply**: Instant application submission
- **Status Tracking**: Real-time application updates

### For Providers
- **Verified Dashboard**: Admin-approved accounts only
- **Scholarship Posting**: Create custom scholarship offerings
- **Applicant Review**: Comprehensive applicant assessment
- **Smart Filtering**: Auto-filters matching applications
- **Analytics**: Track scholarships and applications

### For Administrators
- **Provider Verification**: Approve/reject provider accounts
- **System Oversight**: Monitor all platform activities
- **Quality Control**: Ensure data integrity and security

---

## Technologies

| Version | Technologies |
|---------|-------------|
| **GUI** | Python 3.x, Tkinter, JSON |
| **Terminal** | Python 3.x, CLI, JSON |
| **C++ DSA** | C++11, STL, Text Files |

---

## Learning Outcomes

### GUI & Terminal Versions
- Desktop application development
- Role-based authentication systems
- File-based database operations
- User interface design
- Security (password hashing)

### C++ DSA Version
- Advanced data structures
- Algorithm optimization
- Systems programming
- Performance tuning
- Memory management

---

## Implementation Comparison

| Feature | GUI | Terminal | C++ DSA |
|---------|-----|----------|---------|
| **User Interface** | Graphical | Command-line | Console |
| **Visual Dashboards** | Yes | No | No |
| **Data Storage** | JSON | JSON | Text files |
| **Platform** | Desktop | Desktop/Server | All |
| **Performance** | Good | Fast | Very Fast |
| **Ease of Use** | High | Medium | Low |
| **Learning Value** | Medium | Medium | High |

---

## How IsQueueNek Works

```
Registration (Role Select)
         │
    Approval (if needed)
         │
    Master Profile (Students)
         │
    ├─ Browse Scholarships ─┐  ┌─ Post Scholarships
    │                       │  │
    ├─ Apply (1-click)      │  ├─ Review Applications
    │                       │  │
    └───────┬───────────────┴──┘
            │
    Application Track Status Updates
```

---

## Security Features

- SHA256 password hashing
- Role-based access control
- Admin verification gate
- Document encryption ready
- Session management
- Input validation

---

## System Requirements

### GUI & Terminal Versions
- Python 3.7 or higher
- 50MB free disk space
- tkinter library (included with Python)

### C++ DSA Version
- C++ compiler (GCC, Clang, MSVC)
- C++11 standard support
- 10MB free disk space

---

## Use Cases

**For Students**
- Discover scholarships matching their profile
- Submit applications quickly without repetition
- Track application status in real-time
- Access support and guidance

**For Providers**
- Find eligible applicants automatically
- Review applications efficiently
- Manage scholarship allocations
- Reduce administrative burden

**For Administrators**
- Verify provider legitimacy
- Monitor platform integrity
- Prevent fraud and scams
- Ensure data quality

---

## Statistics

- **Students**: Can apply to unlimited scholarships
- **Providers**: Can post unlimited scholarships
- **Scholarships**: Support unlimited applications
- **Documents**: Unlimited attachment support
- **Performance**: Handles 1000+ records efficiently

---

## Troubleshooting

### GUI Not Starting
```bash
# Install tkinter if missing
python -m pip install tk
```

### Terminal Version Issues
- Ensure Python 3.x is installed
- Check write permissions for data/ folder
- Verify JSON files are not corrupted

### C++ Compilation Issues
```bash
# Use C++11 standard
g++ -std=c++11 IsQueueNek.cpp -o isqueuenek
```

---

## 🔮 Future Enhancements

### Phase 2
- [ ] Email notifications
- [ ] Web-based platform
- [ ] Mobile applications
- [ ] Real-time chat
- [ ] Payment integration

### Phase 3
- [ ] Machine learning matching
- [ ] Cloud deployment
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Video verification

---

## Documentation

- [GUI Implementation Guide](ACP/GUI%20Based%20System/README.md)
- [Terminal CLI Guide](ACP/Terminal%20Based%20System/IsQueueNek/ver_2/README.md)
- [C++ DSA Guide](DSA/README.md)

---

## Tips for Developers

1. **Start with GUI** for understanding the system
2. **Study Terminal** for CLI implementation
3. **Explore C++ DSA** for algorithm optimization
4. **Check data/** folders for sample data
5. **Review security.py** for hashing implementation

---

## License & Status

**Status**: Complete and fully functional
**Version**: 2.0
**Academic Level**: First Year Computer Science
**Last Updated**: June 2026

---

## Support

For questions or issues:
1. Review the specific implementation's README
2. Check source code comments
3. Examine sample data files
4. Consult troubleshooting sections

---

**Project Successfully Demonstrates:**
- Full-stack application design
- Multi-platform implementation
- Database design and operations
- Security best practices
- Algorithm optimization
- User experience design

---

**Ready to use!** Choose your implementation above and get started.
