# Family Care — Health Management System

**Family Care** is a web application built with **Python 3 & Django**, designed for households to manage family member health profiles, medical records, medication schedules, doctor appointments, vitals, AI health risk predictions, and emergency contact IDs.

---

## Features
- **Family Profiles**: Store age, gender, blood group, allergies, chronic conditions, and emergency contacts.
- **Medical Records**: Upload and manage lab reports, doctor notes, prescriptions, and medical imaging documents.
- **Active Medications**: Dosage schedules and refill tracking.
- **Doctor Appointments**: Scheduling and clinic visit reminders.
- **Health Analytics & Vitals**: Track blood pressure, sugar levels (mg/dL), and body weight (kg).
- **AI Health Insights**: Risk predictions for diabetes, cardiovascular, and hypertension health indicators.
- **Emergency SOS**: 1-touch hotline access (Ambulance, Poison Control) and family medical ID cards.

---

## Tech Stack
- **Backend Framework**: Python 3 + Django 5.x
- **Database**: Django ORM with SQLite
- **Frontend**: Django HTML5 Templates + Tailwind CSS + Lucide Icons + HTMX
- **Authentication**: Django `contrib.auth` (Session authentication)

---

## Getting Started

### 1. Requirements
Ensure Python 3.10+ is installed on your machine.

### 2. Installation
Install dependencies specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Start Development Server
```bash
python manage.py runserver 8000
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

### 5. Create Admin Superuser (Optional)
To access the Django Administration portal at `/admin/`:
```bash
python manage.py createsuperuser
```
