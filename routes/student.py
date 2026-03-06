from flask import Blueprint, render_template, redirect
from extensions import db
from models import PlacementDrive, Application, Student
from routes.decorators import role_required
from flask_login import current_user

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@role_required("student")
def dashboard():
    drives = PlacementDrive.query.filter_by(status="Approved").all()
    return render_template("student_dashboard.html", drives=drives)


@student_bp.route("/apply/<int:drive_id>")
@role_required("student")
def apply(drive_id):
    student = Student.query.filter_by(user_id=current_user.id).first()

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if not existing:
        app = Application(student_id=student.id, drive_id=drive_id)
        db.session.add(app)
        db.session.commit()

    return redirect("/student/dashboard")


@student_bp.route("/applications")
@role_required("student")
def view_applications():
    student = Student.query.filter_by(user_id=current_user.id).first()
    apps = Application.query.filter_by(student_id=student.id).all()
    return render_template("student_applications.html", applications=apps)