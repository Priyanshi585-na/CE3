from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_restful import Api,Resource
from flask_jwt_extended import create_access_token, JWTManager
import os
import json
import uuid

app = Flask(__name__) 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my_secret_key" 
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  


# DATABASES
class User(db.Model, UserMixin):
    tablename = "user" 
    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mobile = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    linkedin = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.Integer, nullable=True)   
    preferred_field = db.Column(db.String(100),nullable = False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class Feedback(db.Model):
    tablename = "Feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message
        }
        
        
    def __repr__(self):
        return f"<Feedback {self.name}>"
    
    

class AvailableCourse(db.Model):
    __tablename__ = 'available_courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.name}"
    
    
class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    name = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(500),nullable=False)
    category = db.Column(db.Integer,db.ForeignKey('available_courses.id'),nullable = False)
    difficulty = db.Column(db.String(100),nullable = False)
    price = db.Column(db.Float,nullable=False)
    duration = db.Column(db.Float,nullable = False)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)    
    
    
    def _repr_(self):
        return f"<Course {self.name}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

    
 
with app.app_context():
    db.create_all()
    
        
#APIs    
class AvailableCourseResource(Resource):
    def get(self):
        available_courses = AvailableCourse.query.all()
        course_list=[{
            'id':available_course.id,
            'name':available_course.name            
        }
          for available_course in available_courses]

        return {"courses":course_list}
    
    def post(self):
        data = request.get_json()
        name = data.get('name')

        new_course = AvailableCourse(name=name)
        db.session.add(new_course)
        db.session.commit()

        course_data = {
            'id': new_course.id, 
            'name': new_course.name,
        }
        return course_data, 201 
    
    def put(self,available_course_id):
        course = AvailableCourse.query.get(available_course_id)
        if course:
            data = request.get_json()
            course.name = data.get('name', course.name)

            db.session.commit()
            return {"message": "Course Updated Successfully",
                    "course": {
                        'id': course.id,
                        'name': course.name,
                    }}
        else:
            return {"message": "Course Not Found!"}, 404
        
        
    def delete(self,available_course_id):
        course_to_delete = AvailableCourse.query.get(available_course_id)
        if course_to_delete:
            db.session.delete(course_to_delete)
            db.session.commit()
            return {"message": "Course deleted successfully",
                    "course": {
                        'id': course_to_delete.id,
                        'name': course_to_delete.name
                    }}
        else:
            return {"message": "Course Not Found!"}, 404 


api.add_resource(AvailableCourseResource,'/availablecoursesapi', '/availablecoursesapi/<int:available_course_id>')



class CourseResource(Resource):   
    # @jwt_required 
    def get(self, course_id=None):
        if course_id:
            course = Course.query.filter_by(id=str(course_id)).first()
            course_data = {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'category': course.category,
                'difficulty': course.difficulty,
                'price': course.price,
                'duration': course.duration,
                'created_by': course.created_by
            }
            return {"course": course_data}
        else:
            courses = Course.query.all()
            course_list = [
                {
                    'id': course.id,
                    'name': course.name,
                    'description': course.description,
                    'category': course.category,
                    'difficulty': course.difficulty,
                    'price': course.price,
                    'duration': course.duration,
                    'created_by': course.created_by
                }
                for course in courses
            ]
            return {"courses": course_list}
    
    # @jwt_required
    def post(self):
        data = request.get_json()
        
        id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        difficulty = data.get('difficulty')
        price = data.get('price')
        duration = data.get('duration')
        created_by = data.get('created_by')
        
        new_course = Course(id = id,name=name, description=description, category=category, difficulty=difficulty, price=price, duration=duration, created_by=created_by)
        db.session.add(new_course)
        db.session.commit()

        course_data = {
            'id': new_course.id, 
            'name': new_course.name,
            'description': new_course.description,
            'category': new_course.category,
            'difficulty': new_course.difficulty,
            'price': new_course.price,
            'duration': new_course.duration,
            'created_by': new_course.created_by
        }
        print(course_data['id'])
        return course_data, 201 
    
    def put(self, course_id):
        course = Course.query.filter_by(id=str(course_id)).first()
        if course:
            data = request.get_json()
            course.name = data.get('name', course.name)
            course.price = data.get('price', course.price)
            course.description = data.get('description', course.description)
            course.difficulty = data.get('difficulty', course.difficulty)
            course.category = data.get('category', course.category)
            course.duration = data.get('duration', course.duration)
            course.created_by = data.get('created_by', course.created_by)
            
            db.session.add(course)
            db.session.commit()
            return {"message": "Course Updated Successfully",
                    "course": {
                        'id': course.id,
                        'name': course.name,
                        'price': course.price,
                        'description': course.description,
                        'difficulty': course.difficulty,
                        'category': course.category,
                        'duration': course.duration,
                        'created_by': course.created_by
                    }}
        else:
            return {"message": "Course Not Found!"}, 404
        
    def delete(self, course_id):
        course_to_delete = Course.query.filter_by(id=str(course_id)).first()
        if course_to_delete:
            db.session.delete(course_to_delete)
            db.session.commit()
            return {"message": "Course deleted successfully",
                    "course": {
                        'id': course_to_delete.id,
                        'name': course_to_delete.name,
                        'description': course_to_delete.description,
                        'category': course_to_delete.category,
                        'difficulty': course_to_delete.difficulty,
                        'price': course_to_delete.price,
                        'duration': course_to_delete.duration,
                        'created_by': course_to_delete.created_by
                    }}
        else:
            return {"message": "Course Not Found!"}, 404

api.add_resource(CourseResource, '/coursesapi', '/coursesapi/<string:course_id>')


class FeedbackResource(Resource):
    def post(self):
        data=request.get_json()
        if not data:
            return {'message':'No input data provided'},400
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        new_feedback=Feedback(name=name,email=email,message=message)
        db.session.add(new_feedback)
        db.session.commit()
        
        return {'message':'Feedback given successfully'},201
    
    
    def get(self):
        feedbacks = Feedback.query.all()
        feedback_list = [
            {
                'id': feedback.id,
                'name': feedback.name,
                'message': feedback.message,
                'email':feedback.email
            }
            for feedback in feedbacks
        ]
        return {"feedback":feedback_list}
    
api.add_resource(FeedbackResource,'/feedbackapi')




class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.role)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials."}, 401

api.add_resource(LoginResource, '/loginapi')



class RegisterResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=str(user_id)).first()
            if not user:
                return {"error": "User not found"}, 404  
            
            user_fields = {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'mobile': user.mobile,
                'preferred_field': user.preferred_field,
                'gender': user.gender,
                'role': user.role,
                'linkedin': user.linkedin,
                'experience': user.experience,
            }
            return {"user": user_fields}

        else:
            users = User.query.all()
            user_fields = [{ 
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'mobile': user.mobile,
                'preferred_field': user.preferred_field,
                'gender': user.gender,
                'role': user.role,
                'linkedin': user.linkedin,
                'experience': user.experience,
            } for user in users]

            return {"users": user_fields} 
    
    
    
    
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        mobile = data.get('mobile')
        preferred_field = data.get('preferred_field', []) 
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        gender = data.get('gender')
        role = data.get('role')
        linkedin = data.get('linkedin')
        experience = data.get('experience')

        if not all([id,name, username, email, mobile, password, confirm_password, gender, role]):
            return {'message': 'Missing required fields'}, 400

        if password != confirm_password:
            return {'message': 'Passwords do not match!'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists!'}, 409
        
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists!'}, 409

        if len(mobile) != 10 or not mobile.isdigit():
            return {'message': 'Mobile number must be exactly 10 digits!'}, 400

        if len(password) < 8:
            return {'message': 'Password must be at least 8 characters long.'}, 400


        new_user = User(
            name=name,
            username=username,
            email=email,
            mobile=mobile,
            preferred_field=json.dumps(preferred_field),
            gender=gender,
            role=role,
            linkedin=linkedin,
            experience=experience
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Registration successful!'}, 201
    
    def put(self, user_id):
     user = User.query.filter_by(id=str(user_id)).first()
     if not user:
         return {'message': 'User not found'}, 404
 
     data = request.get_json()
 
     if data.get('name'):
         user.name = data['name']
     if data.get('username'):
         user.username = data['username']
     if data.get('email'):
         user.email = data['email']
     if data.get('mobile'):
         user.mobile = data['mobile']
     if data.get('preferred_field'):
         user.preferred_field = json.dumps(data['preferred_field'])
     if data.get('gender'):
         user.gender = data['gender']
     if data.get('role'):
         user.role = data['role']
     if data.get('linkedin'):
         user.linkedin = data['linkedin']
     if data.get('experience'):
         user.experience = data['experience']
 
     password = data.get('password')
     confirm_password = data.get('confirm_password')
     if password and confirm_password:
         if password != confirm_password:
             return {'message': 'Passwords do not match!'}, 400
         if len(password) < 8:
             return {'message': 'Password must be at least 8 characters long.'}, 400
 
         user.set_password(password) 
 
     db.session.commit()
     return {'message': 'User updated successfully!'}, 200 
    
    
    def delete(self, user_id):
        user = User.query.filter_by(id=str(user_id)).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200


api.add_resource(RegisterResource, '/registerapi','/registerapi/<string:user_id>')




#app routes

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'message' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    feedback = Feedback(name=data['name'], email=data['email'], message=data['message'])
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({"message": "Feedback submitted successfully", "feedback": feedback.to_dict()}), 201

@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedbacks = Feedback.query.all()
    return jsonify([feedback.to_dict() for feedback in feedbacks])



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/teach")
def teach():
    return render_template("teach.html")

@app.route("/teachy")
@login_required
def teachy():
    return render_template("teachy.html")

@app.route("/about")
def about():
    return render_template("aboutus.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")
        role = request.form.get("role")
        preferred_field = request.form.get("preferred_field")
        gender = request.form.get("gender")
        linkedin = request.form.get("linkedin")

       
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        
        if len(mobile) != 10 or not mobile.isdigit():
            flash("Mobile number must be exactly 10 digits!", "danger")
            return redirect(url_for("register"))

      
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("register"))

        if not any(char.isdigit() for char in password):
            flash("Password must contain at least one digit.", "danger")
            return redirect(url_for("register"))

        if not any(char.isalpha() for char in password):
            flash("Password must contain at least one letter.", "danger")
            return redirect(url_for("register"))

        if not any(char in "@$!%?&" for char in password):
            flash("Password must contain at least one special character (@$!%?&).", "danger")
            return redirect(url_for("register"))
            
        
        
        new_user = User(name=name, email=email, mobile=mobile, role=role,username=username,preffered_field=preferred_field,linkedin=linkedin,gender=gender)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("index"))


@app.route('/home')
@login_required
def home():
    data = User.query.all()
    return render_template('home.html', data= data, user=current_user)

@app.route('/python_courses')
@login_required
def python_courses():
    return render_template('python_courses.html')

@app.route('/development')
@login_required
def development():
    return render_template('development.html')



@app.route('/IT_Software')
@login_required
def IT_Software():
    return render_template('IT_Software.html')



@app.route('/programming_languages')
@login_required
def programming_languages ():
    return render_template('programming_languages.html')




@app.route('/othersoftware')
@login_required
def othersoftware ():
    return render_template('othersoftware.html')




@app.route('/datasciencecourses')
@login_required
def datasciencecourses ():
    return render_template('datasciencecourses.html')



@app.route('/javacourses')
@login_required
def javacourses ():
    return render_template('javacourses.html')




@app.route('/dataanalysiscourses')
@login_required
def dataanalysiscourses():
    return render_template('dataanalysiscourses.html')




@app.route('/user')
@login_required
def user():
    data = User.query.all()
    return render_template('user.html', data=data, user=current_user)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user = db.session.get(User, id)
    if user is None:
        return "User  not found", 404

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        
       
        user.name = name
        user.email = email
        user.mobile = mobile
        
        db.session.commit()
        return redirect(url_for("user"))

    return render_template('update.html', user=user)


if __name__ == "__main__":
    app.run(debug = True)