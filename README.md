Transparent, fair billing where every rupee is traceable to actual meals.

---

## Features 

 **Student Profiles** — Track students and room assignments  
 **Meal Attendance** — Mark who ate which meal, which day  
 **Guest Tracking** — Log guests eating at student's expense  
 **Dynamic Pricing** — Normal rates + special rates for specific meals  
 **Transparent Billing** — Students see exactly why they're charged  
 **REST API** — Full API for mobile/web apps  
 **Admin Panel** — Easy Django admin for warden/contractor  
 **Audit Trail** — Monthly bills saved with complete history  

---

## Tech Stack 

- **Backend:** Django 4.x
- **API:** Django REST Framework
- **Database:** SQLite (dev) / PostgreSQL (production-ready)
- **Authentication:** Django built-in User model
- **Admin:** Django admin panel (customized)


## Quick Start 

### 1. Clone Repository
```bash
git clone https://github.com/manpret221/hostel-mess-billing.git
cd Hostel_mess
```

2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install django djangorestframework
```

4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create Admin User
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

## How It Works 

### Daily Flow
1. **Warden marks attendance** → Who ate which meal today
2. **Contractor adds special rates** → If meal cost more
3. **System auto-calculates** → Every student's bill

