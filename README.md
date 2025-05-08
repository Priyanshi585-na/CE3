# Agaahi - Online Course Platform

## Overview
Agaahi is a web-based online course platform designed to provide a rich and interactive learning experience. 

## Features
Agaahi offers a variety of features to enhance the learning experience:
Course Management:Create, update, and delete courses.
Organize courses into categories.
Manage course content, including lessons, videos, and resources.
User Management:User registration and authentication.
Admin panel for user management.

## Architecture
Agaahi's architecture is designed to be modular and scalable. Here's a breakdown of the key components:
Django Backend:Handles the core application logic.Manages the database (models).Provides an admin interface for managing content.Handles user authentication and authorization.
Flask API:Acts as an intermediary between the Django backend and the frontend.Provides API endpoints for data retrieval and manipulation.Ensures a clean separation of concerns between the backend and frontend.
Frontend (HTML, CSS):Provides the user interface for the platform.Interacts with the Flask API to display data and handle user interactions.Ensures a responsive and user-friendly experience.Uses modern HTML and CSS for structure and styling.


## **Installation and Setup**

To set up Agaahi on your local machine, follow these steps:
Prerequisites:
Python 3.xpip (Python package installer)
Virtualenv (recommended)

Clone the repository
source env/bin/activate  # On Linux/macOS
env\Scripts\activate  # On Windows
Install project dependencies: pip install -r requirements.txt 


### **Setup (Flask)**
Navigate to your Flask API directory:cd 'Flask_folder'
Run the Flask development server:python app.py
The Flask API will be accessible at http://localhost:5000/


### **Setup (Django)**
Install Django: 
pip install Django
cd Django/OnlineCoursePlatform

If you don't have a repo, and have the files locally, navigate to the directory
Make migrations: python manage.py makemigrations
Run migrations: python manage.py migrate
Create a superuser: python manage.py createsuperuser
Start the Django development server: python manage.py runserver
The Django backend will be accessible at http://localhost:8000/



Contributions to Agaahi are welcome! 
 Please follow these steps:
 Fork the repository.
 Create a new branch for your feature or bug fix.
 Commit your changes.
 Push to the branch.
 Submit a pull request.# G33OnlineCoursePlatform
