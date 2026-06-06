// IsQueueNek Centralized Scholarship Management System
// A terminal-based application for managing scholarship providers and student applications

#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// Data structure to store scholarship information
struct Scholarship
{
    string name, desc, loc, deadline;
    float min_gwa;
    long long max_income;
    int grant, slots;
    vector<string> applicants;
};

// Data structure to store scholarship provider information
struct Provider
{
    string name, email, contact, address, website, password;
    unordered_map<string, Scholarship> scholarships;
};

// Data structure to store student information
struct Student
{
    string name, address, password;
    int age;
    float gwa;
    long long income;
    vector<string> apps;
};

// Global data structures to store all students and providers
unordered_map<string, Student> students;
unordered_map<string, Provider> providers;

// Utility function to split a string by a delimiter character
vector<string> split(const string &s, char delim)
{
    vector<string> tokens;
    string token;
    istringstream ss(s);
    while (getline(ss, token, delim))
        tokens.push_back(token);
    return tokens;
}

// Get string input from user with a prompt
string get_str(string prompt)
{
    string res;
    cout << prompt;
    getline(cin >> ws, res);
    return res;
}

// Get numeric input from user with a prompt, returns 0 if invalid
float get_num(string prompt)
{
    string res;
    cout << prompt;
    getline(cin >> ws, res);
    try
    {
        return stof(res);
    }
    catch (...)
    {
        return 0;
    }
}

// Load students and providers data from text files into memory
void load_db()
{
    ifstream s_file("students.txt"), p_file("providers.txt");
    string line;

    // Load student records from students.txt
    while (getline(s_file, line))
    {
        if (line.empty())
            continue;

        auto t = split(line, '|');
        if (t.size() >= 7)
        {
            Student s = {t[1], t[6], t[2], (int)stof(t[3]), stof(t[4]), stoll(t[5])};
            if (t.size() >= 8 && !t[7].empty())
                s.apps = split(t[7], ',');
            students[t[0]] = s;
        }
    }

    // Load provider and scholarship records from providers.txt
    while (getline(p_file, line))
    {
        if (line.empty())
            continue;

        auto t = split(line, '|');
        if (t.empty())
            continue;

        // Load provider information
        if (t.size() >= 8 && t[0] == "P")
        {
            providers[t[1]] = {t[2], t[4], t[5], t[6], t[7], t[3]};
        }
        // Load scholarship information linked to a provider
        else if (t.size() >= 11 && t[0] == "S")
        {
            Scholarship sch = {t[3], t[4], t[7], t[10], stof(t[5]), stoll(t[6]), (int)stof(t[8]), (int)stof(t[9])};
            if (t.size() >= 12 && !t[11].empty())
                sch.applicants = split(t[11], ',');
            providers[t[1]].scholarships[t[2]] = sch;
        }
    }
}

// Save all students and providers data back to text files
void save_db()
{
    ofstream s_file("students.txt"), p_file("providers.txt");

    // Write all student records to students.txt
    for (auto &[id, s] : students)
    {
        s_file << id << "|" << s.name << "|" << s.password << "|" << s.age << "|"
               << s.gwa << "|" << s.income << "|" << s.address << "|";
        for (auto &a : s.apps)
            s_file << a << ",";
        s_file << "\n";
    }

    // Write all provider and scholarship records to providers.txt
    for (auto &[pid, p] : providers)
    {
        p_file << "P|" << pid << "|" << p.name << "|" << p.password << "|" << p.email
               << "|" << p.contact << "|" << p.address << "|" << p.website << "\n";
        for (auto &[sid, sch] : p.scholarships)
        {
            p_file << "S|" << pid << "|" << sid << "|" << sch.name << "|" << sch.desc << "|"
                   << sch.min_gwa << "|" << sch.max_income << "|" << sch.loc << "|"
                   << sch.grant << "|" << sch.slots << "|" << sch.deadline << "|";
            for (auto &app : sch.applicants)
                p_file << app << ",";
            p_file << "\n";
        }
    }
}

// Display student dashboard with options to apply and view scholarships
void student_dashboard(string s_id)
{
    while (true)
    {
        Student &s = students[s_id];
        cout << "\n=== STUDENT DASHBOARD (" << s.name << ") ===\n"
             << "[1] Apply Scholarships\n"
             << "[2] My Apps\n"
             << "[3] Logout\n"
             << "Choice: ";

        int choice = get_num("");

        if (choice == 1)
        {
            // Display available scholarships that match student criteria
            cout << "\n--- AVAILABLE SCHOLARSHIPS ---\n";
            for (auto &[pid, p] : providers)
            {
                for (auto &[sid, sch] : p.scholarships)
                {
                    // Check if student meets GWA and income requirements
                    if (s.gwa <= sch.min_gwa && s.income <= sch.max_income)
                    {
                        // Check if student has already applied for this scholarship
                        string sch_ref = pid + "_" + sid;
                        if (find(s.apps.begin(), s.apps.end(), sch_ref) == s.apps.end())
                        {
                            cout << pid << "_" << sid << " : " << sch.name << " by " << p.name << " (Grant: PHP" << sch.grant << ")\n";
                        }
                    }
                }
            }
            string ref = get_str("Enter ID (ProvID_SchlID) to apply or 'B' back: ");
            if (ref != "B" && ref != "b")
            {
                // Apply to selected scholarship
                auto t = split(ref, '_');
                if (t.size() == 2 && providers.count(t[0]) && providers[t[0]].scholarships.count(t[1]))
                {
                    s.apps.push_back(ref);
                    providers[t[0]].scholarships[t[1]].applicants.push_back(s_id);
                    save_db();
                    cout << "Applied!\n";
                }
                else
                    cout << "Invalid ID.\n";
            }
        }
        else if (choice == 2)
        {
            // Display all scholarships the student has applied to
            cout << "\n--- MY APPLICATIONS ---\n";
            for (auto &ref : s.apps)
            {
                auto t = split(ref, '_');
                cout << "- " << providers[t[0]].scholarships[t[1]].name << " (" << providers[t[0]].name << ")\n";
            }
        }
        else
            break;
    }
}

// Display provider dashboard with options to create scholarships and view applicants
void provider_dashboard(string p_id)
{
    while (true)
    {
        Provider &p = providers[p_id];
        cout << "\n=== PROVIDER DASHBOARD (" << p.name << ") ===\n"
             << "[1] Create Scholarship\n"
             << "[2] View Applicants\n"
             << "[3] Logout\n"
             << "Choice: ";

        int choice = get_num("");

        if (choice == 1)
        {
            // Create a new scholarship with user-provided details
            string s_id = "SCH-" + to_string(p.scholarships.size() + 1);
            p.scholarships[s_id] = {get_str("Name: "), get_str("Desc: "), get_str("Location: "),
                                    get_str("Deadline (YYYY-MM-DD): "), get_num("Min GWA: "),
                                    (long long)get_num("Max Income: "), (int)get_num("Grant: "),
                                    (int)get_num("Slots: ")};
            save_db();
            cout << "Created " << s_id << "!\n";
        }
        else if (choice == 2)
        {
            // Display all scholarships and their applicants
            for (auto &[sid, sch] : p.scholarships)
            {
                cout << "\nScholarship: " << sch.name << " (" << sid << ")\n";
                for (auto &a_id : sch.applicants)
                {
                    Student &s = students[a_id];
                    cout << " - " << s.name << " (ID: " << a_id << ", GWA: " << s.gwa << ")\n";
                }
            }
        }
        else
            break;
    }
}

// Handle login for students and providers
void login_register(bool is_student)
{
    string id = get_str("ID: "), pass = get_str("Password: ");
    if (is_student)
    {
        // Verify student credentials and access student dashboard
        if (students.count(id) && students[id].password == pass)
            student_dashboard(id);
        else
            cout << "Invalid Login.\n";
    }
    else
    {
        // Verify provider credentials and access provider dashboard
        if (providers.count(id) && providers[id].password == pass)
            provider_dashboard(id);
        else
            cout << "Invalid Login.\n";
    }
}

// Handle registration for new students and providers
void register_user(bool is_student)
{
    string pass = get_str("Set Password: ");
    if (is_student)
    {
        // Register a new student and generate unique ID
        string id = "26-" + to_string(students.size() + 1);
        students[id] = {get_str("Name: "), get_str("Address: "), pass,
                        (int)get_num("Age: "), get_num("GWA: "), (long long)get_num("Income: ")};
        cout << "Registered! Your ID: " << id << "\n";
    }
    else
    {
        // Register a new provider and generate unique ID
        string id = "PROV-" + to_string(providers.size() + 1);
        providers[id] = {get_str("Org Name: "), get_str("Email: "), get_str("Contact: "),
                         get_str("Address: "), get_str("Website: "), pass};
        cout << "Registered! Your ID: " << id << "\n";
    }
    save_db();
}

// Main menu - entry point of the application
int main()
{
    load_db();
    while (true)
    {
        // Display main menu options
        cout << "\n=== ISQUEUENEK SCHOLARSHIP SYSTEM ===\n"
             << "[1] Student Login\n"
             << "[2] Student Register\n"
             << "[3] Provider Login\n"
             << "[4] Provider Register\n"
             << "[5] Exit\n"
             << "Choice: ";

        int choice = get_num("");

        if (choice == 1)
            login_register(true);
        else if (choice == 2)
            register_user(true);
        else if (choice == 3)
            login_register(false);
        else if (choice == 4)
            register_user(false);
        else
            break;
    }
    return 0;
}