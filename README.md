# Agaahi - Online Course Platform

## Overview
Agaahi is a web-based online course platform designed to provide a rich and interactive learning experience. 

## Features
Agaahi offers a variety of features to enhance the learning experience:
- Course Management:Create, update, and delete courses.
- Organize courses into categories.
- Manage course content.
- User Management:User registration and authentication.
- Admin panel for user management.

## Architecture
Agaahi's architecture is designed to be modular and scalable. Here's a breakdown of the key components:

- Django Backend: Handles the core application logic.Manages the database (models).Provides an admin interface for managing content.Handles user authentication and authorization.
- Flask API: Acts as an intermediary between the Django backend and the frontend.Provides API endpoints for data retrieval and manipulation.
- Frontend (HTML, CSS): Provides the user interface for the platform.


## **Installation and Setup**

To set up Agaahi on your local machine, follow these steps:

### Prerequisites:

- Python 3.xpip (Python package installer)

- Virtualenv (recommended)

### Clone the repository
```bash
git clone https://github.com/Priyanshi585-na/OnlineCoursePlatform.git
cd OnlineCoursePlatform
```



### Activate environmnent

(If you are working on Linux/macOS)
```bash 
source env/bin/activate    
```


(If on Windows)
```bash
env\Scripts\activate 
```

Install project dependencies:

```bash
pip install -r requirements.txt 
```

### **Setup (Flask)**
Navigate to your Flask API directory:
```bash
cd Flask-flask
```


Run the Flask development server: 
```bash
python app.py
```

The Flask API will be accessible at http://localhost:5000/


### **Setup (Django)**

```bash
cd Django/OnlineCoursePlatform
```

Make migrations and run them: 

```bash
python manage.py makemigrations

python manage.py migrate
```


Create a superuser and run the development server:

```bash
python manage.py createsuperuser

 python manage.py runserver
```


The Django backend will be accessible at http://localhost:8000/



### Contributions to Agaahi are welcome! 

 Please follow these steps:
 
 Fork the repository.
 
 Create a new branch for your feature or bug fix.
 
 Commit your changes.
 
 Push to the branch.
 
 Submit a pull request.# G33OnlineCoursePlatform
