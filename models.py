from extensions import db
from flask_login import UserMixin
from datetime import datetime


# -----------------------
# USER MODEL
# -----------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/student/company
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -----------------------
# STUDENT MODEL
# -----------------------
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    phone = db.Column(db.String(20))
    course = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    resume_path = db.Column(db.String(200))


# -----------------------
# COMPANY MODEL
# -----------------------
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(150))

    approved = db.Column(db.Boolean, default=False)
    blacklisted = db.Column(db.Boolean, default=False)


# -----------------------
# PLACEMENT DRIVE MODEL
# -----------------------
class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.String(200))

    application_deadline = db.Column(db.Date)

    status = db.Column(db.String(20), default="Pending")
    # Pending / Approved / Closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -----------------------
# APPLICATION MODEL
# -----------------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)

    status = db.Column(db.String(30), default="Applied")
    # Applied / Shortlisted / Selected / Rejected

    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )