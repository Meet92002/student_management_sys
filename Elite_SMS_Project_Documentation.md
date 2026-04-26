# Elite SMS (Student Management System) - Project Documentation

## 1. Introduction
**Elite SMS** is a comprehensive, full-stack web application built to streamline and digitize academic administration. Developed using **Python, Flask, and MySQL**, the system provides dedicated interfaces for Admins, Professors, and Students. It handles everything from user authentication and attendance tracking to assignment submissions and automated quiz grading, making it a complete solution for modern educational institutions.

## 2. Project Brief
The objective of this project was to build a scalable, secure, and user-friendly portal to manage complex academic relationships. 
* **Evolution:** The project initially started with a JSON-based file storage system to establish the core logic, which was later migrated to an **SQLite** database, and finally scaled to a production-ready **MySQL** database.
* **Architecture:** It follows a modular architecture, separating database models (`models.py`), business logic (`services/`), and routing (`app.py`), ensuring the codebase remains maintainable and scalable.
* **Focus:** A heavy emphasis was placed on creating a premium, responsive User Interface (UI) featuring dark mode, glassmorphism, and dynamic data visualization.

---

## 3. Feature List & Core Logic

| Feature | Description | Business Logic / Conditions |
| :--- | :--- | :--- |
| **Authentication & RBAC** | Secure login/sign-up system with distinct roles (Admin, Professor, Student). | **Logic:** Uses `Werkzeug` for password hashing. <br>**Condition:** Custom Python decorators (`@admin_required`, `@professor_required`) verify `current_user.role`. If unauthorized, redirects to the dashboard with a Flash error. |
| **Student Dashboard** | Real-time analytics for students including attendance, pending work, and grades. | **Logic:** Calculates attendance: `(present_days / total_days) * 100`.<br>**Condition:** Averages the student's grades by subject to render a dynamic performance graph. |
| **Professor Dashboard** | Customized view for professors to manage their specific subjects and grading. | **Logic:** Filters database for assignments where `prof_id == current_user.id`.<br>**Condition:** Counts pending submissions specifically linked to their created assignments. |
| **Assignment Engine** | Platform for creating assignments, submitting work, and grading. | **Logic:** Submission creates a record linking `student_id` and `assignment_id` with status "Submitted".<br>**Condition:** When graded, status becomes "Graded" and the score automatically updates the student's global Grade record. |
| **Automated Quizzes** | Multiple-choice quiz creation and instant auto-grading engine. | **Logic:** Compares student's selected options with the `is_correct` database boolean.<br>**Security:** Students can only view and take quizzes for subjects they are currently enrolled in. If not enrolled in any subjects, no quizzes will be visible. |
| **Library Tracker** | Admin tool to manage and track borrowed library books. | **Logic:** Links book records to student profiles.<br>**Condition:** Updates status between "Borrowed" and "Returned". |

---

## 4. SQL & Database Architecture

The project utilizes **SQLAlchemy ORM** over a **MySQL** database. This maps Python objects to tables and prevents SQL injection.

### Key Tables & Relationships
| Table Name | Purpose | Foreign Key Relationships |
| :--- | :--- | :--- |
| `User` | Base authentication table | None |
| `Student` | Profile data for students | Extends `User.id` |
| `Staff` | Profile data for professors | Extends `User.id` |
| `Assignment` | Tasks created by professors | Links to `Staff.id` (`prof_id`) |
| `Submission` | Student answers for assignments | Links to `Assignment.id` and `Student.id` |
| `Quiz` | Multiple-choice exams | Links to `Staff.id` (`prof_id`) |

### Query Logic & Optimizations

| Optimization Type | Python/Inefficient Method | SQL/Optimized Method (Implemented) |
| :--- | :--- | :--- |
| **Direct Filtering** | `[a for a in assignments if a.prof_id == user_id]` | `Assignment.query.filter_by(prof_id=user_id).all()` |
| **Bulk Lookups** | `for s in subs: if s.assign_id in my_list:` | `Submission.query.filter(Submission.assignment_id.in_(my_assign_ids)).all()` |

---

## 5. Frontend Design (HTML/CSS & Jinja2 Logic)

### UI/UX Design (Vanilla CSS)
The frontend relies on custom **Vanilla CSS** for maximum control and a premium aesthetic without heavy frameworks.
* **CSS Variables (`:root`)**: Enables seamless Dark Mode by swapping variable hex codes via JavaScript.
* **Glassmorphism**: Utilizes rounded borders (`border-radius: 16px`), soft drop shadows (`box-shadow`), and clean spacing to create a tactile feel.

### Conditional Rendering (Jinja2)
The application uses the **Jinja2 templating engine** to seamlessly inject backend Python logic directly into the HTML structure.

| Jinja2 Concept | Syntax Example | Usage / Logic |
| :--- | :--- | :--- |
| **Role-Based UI** | `{% if current_user.role == 'admin' %}` | Dynamically hides/shows navigation menu links depending on the logged-in user's role. |
| **Dynamic Alerts** | `{% for category, message in messages %}` | Intercepts Flask Flash messages and applies CSS classes based on the category (e.g., `success` vs `danger`). |
| **Data Loops** | `{% for row in leaderboard %}` | Iterates through Python lists/dictionaries to automatically generate HTML table rows without hardcoding. |

---
*Document prepared for Technical Interview Presentation.*
