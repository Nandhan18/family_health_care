# Family Care — Health Management System

**Family Care** is a comprehensive health management application structured into decoupled **`frontend/`** and **`backend/`** folders, designed for households to manage family member health profiles, medical records, medication schedules, doctor appointments, vitals, AI health risk predictions, and emergency contact IDs.

---

## Directory Structure

```text
Family Care/
├── frontend/             # Frontend UI assets, templates, stylesheets, and scripts
│   ├── templates/        # HTML templates for views & pages
│   ├── static/           # CSS stylesheets and JavaScript client files
│   ├── package.json      # Frontend package configuration
│   └── README.md
│
├── backend/              # Python & Django backend service
│   ├── apps/             # Modular feature Django apps (accounts, members, records, etc.)
│   ├── family_care/      # Core Django settings & configuration
│   ├── manage.py         # Django CLI management script
│   ├── requirements.txt  # Python backend dependencies
│   └── README.md
│
└── README.md             # Project documentation
```

---

## Features
- **Admin Dashboard & Management Console**: Dedicated administrator portal (`/admin-dashboard/` or `/admin-login/`) with separate admin credentials to inspect all user details, total family members, medical records, medications, appointments, and execute administrative actions (grant/revoke admin status, reset user passwords, activate/deactivate accounts, create or delete user profiles).
- **Family Profiles**: Store age, gender, blood group, allergies, chronic conditions, and emergency contacts.
- **Medical Records**: Upload and manage lab reports, doctor notes, prescriptions, and medical imaging documents.
- **Active Medications**: Dosage schedules and refill tracking.
- **Doctor Appointments**: Scheduling and clinic visit reminders.
- **Health Analytics & Vitals**: Track blood pressure, sugar levels (mg/dL), and body weight (kg).
- **AI Health Insights**: Risk predictions for diabetes, cardiovascular, and hypertension indicators with point-wise actionable recommendations.
- **Emergency SOS**: 1-touch hotline access (Ambulance, Poison Control) and family medical ID cards.

---

## Administrator Access & Credentials

To log into the **Admin Portal**, access `/admin-login/` or click **Admin Portal** from the header navigation bar.

### Default Admin Credentials:
- **Username**: `Nandhan` (or `admin`)
- **Password**: `Nandhan1234` (or `admin1234`)

### Create Custom Admin via CLI:
```bash
python manage.py create_admin --username <your_username> --password <your_password>
```

---

## Tech Stack
- **Backend Framework**: Python 3 + Django 5.x
- **Database**: Django ORM with SQLite
- **Frontend**: Django HTML5 Templates + Tailwind CSS + Lucide Icons
- **Authentication**: Django `contrib.auth` (Session authentication)

---

## Getting Started

### 1. Backend Setup (Django)

Navigate to the `backend/` folder:
```bash
cd backend
```

Install backend Python dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations:
```bash
python manage.py migrate
```

Start the backend server:
```bash
python manage.py runserver 8000
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

### 2. Frontend Setup

The frontend templates and static assets in `frontend/` are loaded by Django. For frontend asset management or development:
```bash
cd frontend
npm install
```
