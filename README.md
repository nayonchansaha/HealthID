# HealthID
#### Video Demo: (https://youtu.be/wXIv9aA7Fys)
#### Description:

## What is HealthID?

HealthID is a web-based medical record management system built with Python, Flask, SQL, and Bootstrap. The core idea behind this project came from a very real problem that affects millions of people in Bangladesh and across the developing world — the loss and mismanagement of medical records. Patients carry paper prescriptions and test reports to every doctor visit. These papers get lost, damaged, or forgotten at home. When a patient visits a new doctor or goes to a hospital in an emergency, they often have nothing to show. This leads to repeated tests, delays in treatment, and sometimes dangerous medical decisions made without proper history.

HealthID solves this by giving every patient a unique digital ID — formatted as HID-2026-XXXXX — that stores all their medical records in one secure place. The patient never needs to carry paper again. Any doctor or hospital can access the records instantly using just the HealthID number.

---

## How It Works

HealthID has two distinct sides — one for patients and one for doctors or hospitals.

**For Patients:** A patient registers once on the platform by providing their name, username, password, blood group, age, and phone number. Upon registration, the system automatically generates a unique HealthID for them. This ID is permanently associated with their account. After logging in, the patient can upload their medical records — prescriptions, test reports, or any other documents — as PDF or image files (JPG, PNG, JPEG). Each record has a title, an optional description, and a timestamp. The patient can view all their uploaded records on their dashboard and download any file whenever needed.

**For Doctors and Hospitals:** A doctor or hospital staff member does not need to create any account or log in. They simply visit the Search page, enter the patient's HealthID, and instantly see the patient's full profile — name, age, blood group, phone number — along with all uploaded medical records. They can open and view files but cannot upload, edit, or delete anything. This read-only access protects the integrity of patient data while making it easily accessible to medical professionals.

---

## Files and Structure

**app.py** — This is the main Flask application file. It contains all the route definitions and the core logic of the project. The routes include `/` for the homepage and patient dashboard, `/register` for new patient registration, `/login` and `/logout` for session management, `/upload` for adding new medical records, and `/search` for the doctor-facing patient lookup. The file also contains three helper functions: `get_db()` which connects to the SQLite database, `allowed_file()` which validates uploaded file extensions, and `generate_health_id()` which creates a unique HealthID using a random 5-digit number.

**helpers.py** — This file contains the `login_required` decorator which protects routes that should only be accessible to logged-in users. It redirects unauthenticated users to the login page.

**health.db** — This is the SQLite database file. It contains two tables. The `users` table stores each patient's id, health_id, name, username, hashed password, blood group, age, and phone number. The `records` table stores each uploaded medical record with its id, user_id (foreign key referencing users), title, description, file path, and upload timestamp.

**templates/home.html** — The public homepage that greets visitors with two options: one for patients to login or register, and one for doctors to search patients. This page is visible without any login.

**templates/layout.html** — The base template that all other templates extend. It contains the navbar, Bootstrap CSS and JS links, and the custom stylesheet link.

**templates/login.html** — The patient login page with username and password fields.

**templates/register.html** — The patient registration form collecting name, username, password, blood group, age, and phone number.

**templates/index.html** — The patient dashboard shown after login. Displays the patient's profile card with their HealthID badge and a list of all their uploaded medical records.

**templates/upload.html** — The form for uploading a new medical record with a title, optional description, and file.

**templates/search.html** — The doctor-facing search page. Accepts a HealthID and displays the matching patient's profile and records in read-only format.

**static/style.css** — Custom CSS that enhances the Bootstrap styling with a consistent blue color scheme, card hover effects, rounded buttons, and the HealthID badge styling.

**static/uploads/** — The folder where all uploaded medical files are stored on the server.

---

## Design Decisions

**Why separate patient and doctor views?** Early in the design process, I considered requiring doctors to also create accounts. However, this would create a barrier in emergency situations where time is critical. A doctor should be able to access patient records immediately without any registration process. The read-only restriction ensures that only the patient themselves can manage their own records.

**Why store files in static/uploads?** Flask can serve files from the static folder directly without additional configuration. This made file serving simpler and more reliable, especially in the CS50 development environment.

**Why use SQLite instead of a larger database?** For the scope of this project, SQLite is sufficient and requires no additional server setup. It integrates seamlessly with Python and Flask.

**Why Bootstrap?** The target users of HealthID include patients and doctors in Bangladesh who may access the system from mobile phones. Bootstrap ensures the interface is fully responsive and works well on all screen sizes.

**Why Bangla in the UI?** The interface uses Bangla language because the target users are patients and medical staff in Bangladesh who are more comfortable with their native language. This makes the application more accessible and practical for real-world use.

---

## Conclusion

HealthID is a practical solution to a real problem. It is simple enough for anyone to use, yet powerful enough to make a genuine difference in how people manage their health information. Building this project taught me how to combine Flask routing, SQLite databases, file handling, and session management into a complete, functional web application. I am proud of what I built and I hope it demonstrates everything I have learned in CS50.
