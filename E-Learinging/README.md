# E-Learn Premium Platform

A high-performance, modern E-Learning management system built with Django.

## ✨ Features
- **4 Dedicated Roles**: Super Admin, Admin, Faculty, and Student.
- **Glassmorphism UI**: Beautiful, premium interface with smooth animations and gradients.
- **Course Management**: Advanced course listing, detailed previews, and one-click enrollment.
- **Content Delivery**: Support for Video lectures and PDF materials.
- **Assessment Engine**: Interactive Quiz system with automated scoring and result tracking.
- **Progress Tracking**: Real-time progress monitoring for students.
- **Role-Based Dashboards**: Personalized experiences for each user type.

## 🚀 Setup Instructions

1. **Install Dependencies** (Ensure Python and Django are installed)
   ```bash
   pip install django
   ```

2. **Navigate to Project Directory**
   ```bash
   cd elearning_project
   ```

3. **Run Migrations** (Already performed by Antigravity)
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser** (Important)
   ```bash
   python manage.py createsuperuser
   ```
   *Follow the prompts to set up your username and password.*

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the App**
   - Main Page: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

## 📂 Project Structure
- `accounts/`: User authentication, roles, and profiles.
- `courses/`: Course management and enrollment logic.
- `quiz/`: Quiz creation and taking engine.
- `materials/`: PDF and document management.
- `videos/`: Video lecture support.
- `results/`: Student performance tracking.
- `progress/`: Course completion monitoring.

## 🎨 Aesthetics
The platform uses a custom design system based on:
- **Primary Color**: Indigo (#6366f1)
- **Secondary Color**: Pink (#ec4899)
- **Glassmorphism**: 12px blur with semi-transparent slates.
- **Typography**: Outfit (Google Fonts).
- **Icons**: Lucide Icons.
