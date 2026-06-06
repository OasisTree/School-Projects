# First-Year Computer Science Projects

**Welcome to the First-Year Project Portfolio** — A comprehensive collection of academic projects demonstrating proficiency in web development, desktop application design, and systems programming.

---

## Project Overview

This repository contains three major projects developed during the first year of computer science studies, showcasing progressive skill development across multiple domains:

| Project | Type | Technologies | Status |
|---------|------|-------------|--------|
| [Di-Budol Website](#di-budol-website) | Web Development | HTML5, CSS3 | Complete |
| [CampusConnect](#campusconnect-student-engagement-portal) | Desktop Application | Python, Tkinter | Complete |
| [IsQueueNek](#isqueuenek-centralized-scholarship-system) | Desktop Application & Systems | Python, C++, Tkinter | Complete |

---

## Di-Budol Website

### Overview
A responsive, multi-page educational web platform promoting digital literacy and online safety awareness, with special focus on orphan welfare advocacy in the Philippines.

### Key Features
- **Educational Content**: Digital literacy and cybersecurity resources
- **Learning Center**: Curated video tutorials and learning materials
- **Community Support**: Counseling services and resource directory
- **Responsive Design**: Optimized for all device sizes
- **Accessible UI**: High contrast design with smooth animations

### Technologies
- **Frontend**: HTML5, CSS3
- **Styling**: CSS3 Media Queries, Font Awesome, Google Fonts
- **Version Control**: Git

### Quick Start
```bash
# Option 1: Direct browser
Open Di_Budol_Website/index.html in your browser

# Option 2: Local server (Python 3)
cd Di_Budol_Website
python -m http.server 8000
# Visit http://localhost:8000
```

[Full Documentation](Di_Budol_Website/README.md)

---

## CampusConnect – Student Engagement Portal

### Overview
A comprehensive desktop application providing a centralized hub for campus communication, event management, and student-organization collaboration through an intuitive graphical interface.

### Key Features
- **Secure Authentication**: SHA256 password hashing, role-based access
- **Event Management**: Create, publish, and track campus events
- **Organization Management**: Student groups and team coordination
- **Direct Messaging**: Real-time communication between users
- **Role-Based Dashboards**: Student, Organization, and Admin views
- **Notifications System**: Real-time alerts and updates
- **Form Management**: Create surveys and collect responses

### Technologies
- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Data Storage**: JSON-based file persistence
- **Security**: SHA256 hashing, UUID generation

### Quick Start
```bash
cd Hackathon_Campus_Connect_Team_Beat
python app.py
```

[Full Documentation](Hackathon_Campus Connect _Team Beat/README.md)

---

## IsQueueNek – Centralized Scholarship Management System

### Overview
A comprehensive, multi-platform scholarship discovery and management system serving as a centralized hub connecting student applicants with verified scholarship providers. Available in both desktop GUI and terminal-based implementations, with a C++ data structures version for advanced algorithms.

### Key Features

#### For Students
- **Master Student Profile**: Store information once, apply to multiple scholarships
- **Document Management**: Upload PDFs and images for verification
- **Automated Eligibility Screening**: Smart filtering based on GWA, income, location
- **One-Click Application**: Apply to eligible scholarships instantly
- **Application Tracking**: Monitor real-time status

#### For Providers
- **Verified Dashboard**: Secure access after Admin approval
- **Scholarship Creation**: Define requirements and eligibility criteria
- **Automated Slot Management**: Track available slots automatically
- **Applicant Review**: Filter and assess applications

### Technologies
- **GUI Version**: Python 3.x + Tkinter
- **Terminal Version**: Python 3.x CLI
- **DSA Version**: C++ with STL
- **Data Storage**: JSON files (Python), Text files (C++)

### Quick Start
```bash
# GUI Version
cd IsQueueNek_Centralized_Scholarship_System/ACP/GUI\ Based\ System
python main.py

# Terminal Version
cd IsQueueNek_Centralized_Scholarship_System/ACP/Terminal\ Based\ System/IsQueueNek/ver_2
python main.py

# C++ DSA Version
cd IsQueueNek_Centralized_Scholarship_System/DSA
g++ -std=c++11 IsQueueNek.cpp -o isqueuenek
./isqueuenek
```

[Full Documentation](IsQueueNek_Centralized_Scholarship_System/README.md)  
[DSA Documentation](IsQueueNek_Centralized_Scholarship_System/DSA/README.md)

---

## Quick Start Guide

### Running All Projects

#### 1. Di-Budol Website
```bash
cd Di_Budol_Website
python -m http.server 8000
```

#### 2. CampusConnect
```bash
cd Hackathon_Campus_Connect_Team_Beat
python app.py
```

#### 3. IsQueueNek GUI
```bash
cd IsQueueNek_Centralized_Scholarship_System/ACP/GUI\ Based\ System
python main.py
```

---

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Projects** | 3 |
| **Languages** | 4 (HTML, CSS, Python, C++) |
| **Database Files** | 15+ JSON/Text files |
| **GUI Screens** | 12+ |

---

## Learning Outcomes

### Web Development
- Responsive design principles
- CSS animations and transitions
- Semantic HTML5 structure
- Accessibility best practices

### Desktop Applications
- GUI framework usage (Tkinter)
- State management and session handling
- File-based data persistence
- Role-based access control
- Password hashing and security

### Systems Programming
- Data structures (Maps, Vectors, Trees)
- Algorithm optimization
- Object-oriented design
- File I/O operations

---

## Development Requirements

### General
- Python 3.7+
- Git for version control

### Desktop Applications
- Python 3.x
- tkinter (included with Python)

### Systems Programming
- C++ compiler (g++, clang, MSVC)
- C++11 or later standard

---

## License

These projects are part of academic coursework for first-year computer science studies.

---

## Project Status

- Di-Budol Website - Complete
- CampusConnect - Complete
- IsQueueNek GUI - Complete
- IsQueueNek CLI - Complete
- IsQueueNek C++ DSA - Complete
- Comprehensive Documentation - Complete

---

**Last Updated**: June 2026  
**Status**: All Projects Active and Complete  
**Version**: 1.0  
**Academic Level**: First Year Computer Science
