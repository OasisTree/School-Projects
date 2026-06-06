# IsQueueNek Centralized Scholarship Management System

## Overview
**IsQueueNek** is a fast, terminal-based application written in C++ that bridges the gap between scholarship providers and students. It centralizes the process of posting, searching, and managing scholarships, utilizing C++ for efficient memory management and quick access.

---

## Key Features

### For Students
* **Profile Management:** Register a secure account and store essential academic data (GWA, income, address).
* **Smart Search:** Automatically filter and view scholarships based on your eligibility.
* **Application Tracking:** Apply to opportunities and easily track your active applications.

### For Providers
* **Organization Setup:** Create a provider profile with full contact details and website links.
* **Scholarship Creation:** Post new grants with specific minimum GWA, maximum income limits, and deadlines.
* **Applicant Review:** Access a real-time list of all students who have applied to your postings.

---

## Technical Architecture

* **Data Structures:** The system relies heavily on `unordered_map` for fast, key-based access to Student and Provider records, and `vector` for managing dynamic lists (like tracking who applied to what).
* **Data Persistence:** Data is saved locally using pipe-delimited text files (`students.txt`, `providers.txt`). 
* **Data Flow:** 
  1. **Load:** `load_db()` parses the text files line-by-line at startup and loads them into memory.
  2. **Runtime:** All actions occur in memory for optimal speed.
  3. **Save:** `save_db()` converts the vectors and maps back into delimited strings and overwrites the text files upon exiting.

---

## How to Use

1. Run the application.
2. Select your role from the main menu: **Student** or **Provider**.
3. Log in with existing credentials or register a new account.
4. Navigate your dashboard:
   * **Students:** Browse eligible scholarships and submit applications.
   * **Providers:** Post new scholarships and check applicant lists.
5. Exit the program safely to trigger the automatic data save.

---

## Sample Accounts

### Student
| Name                | ID   | Password |
| ------------------- | ---- | -------- |
| Dylan Luke P. Oatis | 26-1 | test123  |

### Providers
| Organization                                | ID     | Password    |
| ------------------------------------------- | ------ | ----------- |
| Department of Science and Technology (DOST) | PROV-1 | dost123     |
| Commission on Higher Education (CHED)       | PROV-2 | ched123     |
| Provincial Government of Batangas           | PROV-3 | batangas123 |
| City Government of Lipa                     | PROV-4 | lipa123     |
